# -*- coding: UTF-8 -*-
#A part of the IndentNav addon for NVDA
#Copyright (C) 2017-2024 Tony Malykh
#This file is covered by the GNU General Public License.
#See the file LICENSE  for more details.

# This addon allows to navigate documents by indentation or offset level.
# In editable text fields you can navigate by the indentation level.
# This is useful for editing source code.
# Author: Tony Malykh <anton.malykh@gmail.com>
# https://github.com/mltony/nvda-indent-nav/
# Original author: Sean Mealin <spmealin@gmail.com>

import addonHandler
import api
from appModules.devenv import VsWpfTextViewTextInfo
from compoundDocuments import CompoundTextInfo
import controlTypes
import config
from NVDAObjects.IAccessible.chromium import ChromeVBufTextInfo

try:
    from config.configFlags import ReportLineIndentation
except (ImportError, ModuleNotFoundError):
    pass
import core
import ctypes
from enum import Enum, auto
import globalCommands
import globalPluginHandler
import gui
from gui.settingsDialogs import SettingsPanel
from gui import guiHelper, nvdaControls
import inputCore
import json
import keyboardHandler
from logHandler import log
import NVDAHelper
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.IAccessible import IA2TextTextInfo
from NVDAObjects.IAccessible.ia2TextMozilla import MozillaCompoundTextInfo
from NVDAObjects import NVDAObject, NVDAObjectTextInfo
import operator
import os
import queue
import re
import scriptHandler
from scriptHandler import script
import speech
import struct
import subprocess
import textInfos
from textInfos import UNIT_CHARACTER
from textInfos.offsets import OffsetsTextInfo
import threading
import time
import tones
from typing import Tuple
import ui
from utils.displayString import DisplayStringIntEnum
import versionInfo
import winUser
import wx
import dataclasses
from . import textUtils

try:
    ROLE_EDITABLETEXT = controlTypes.ROLE_EDITABLETEXT
    ROLE_TREEVIEWITEM = controlTypes.ROLE_TREEVIEWITEM
except AttributeError:
    ROLE_EDITABLETEXT = controlTypes.Role.EDITABLETEXT
    ROLE_TREEVIEWITEM = controlTypes.Role.TREEVIEWITEM

BUILD_YEAR = getattr(versionInfo, "version_year", 2023)

debug = False
if debug:
    LOG_FILE_NAME = r"H:\\2.txt"
    f = open(LOG_FILE_NAME, "w", encoding='utf=8')
    f.close()
    LOG_MUTEX = threading.Lock()
    def mylog(s):
        with LOG_MUTEX:
            f = open(LOG_FILE_NAME, "a", encoding='utf-8')
            print(s, file=f)
            f.close()
else:
    def mylog(*arg, **kwarg):
        pass


# Adapted from NVDA's speech module to count tabs as blank characters.
BLANK_CHUNK_CHARS = frozenset((" ", "\n", "\r", "\t", "\0", u"\xa0"))
def isBlank(text):
    return not text or set(text) <= BLANK_CHUNK_CHARS


def myAssert(condition):
    if not condition:
        raise RuntimeError("Assertion failed")

class IndentNavKeyMap(DisplayStringIntEnum):
    LAPTOP = 0
    ALT_NUMPAD = 1
    NUMPAD = 2
    NUMPAD_ALT_REVIEW = 3

    @property
    def _displayStringLabels(self):
        return {
            IndentNavKeyMap.LAPTOP: _("Laptop or legacy key map: NVDA+alt+arrows"),
            IndentNavKeyMap.ALT_NUMPAD: _("Alt+numPad"),
            IndentNavKeyMap.NUMPAD: _("Numpad assigned to IndentNav in editables; numPad assigned to review cursor everywhere else"),
            IndentNavKeyMap.NUMPAD_ALT_REVIEW: _("Numpad assigned to IndentNav; review cursor commands remapped to alt+NumPad"),
        }


IN_KEY_MAPS_SOURCE = {
    'moveToNextSibling': [
        'NVDA+alt+DownArrow',
        'numpad2',
    ],
    'moveToNextSiblingSkipClutter': [
        'NVDA+alt+windows+DownArrow',
        'control+numpad2',
    ],
    'moveToNextSiblingForce': [
        'NVDA+alt+control+DownArrow',
        'control+numpad6',
    ],
    'moveToPreviousSibling': [
        'NVDA+alt+UpArrow',
        'numpad8',
    ],
    'moveToPreviousSiblingSkipClutter': [
        'NVDA+windows+alt+UpArrow',
        'control+numpad8',
    ],

    'moveToPreviousSiblingForce': [
        'NVDA+alt+control+UpArrow',
        'control+numpad4',
    ],
    'moveToLastSibling': [
        'NVDA+alt+shift+DownArrow',
        'numpad6',
    ],
    'moveToFirstSibling': [
        'NVDA+alt+shift+UpArrow',
        'numpad4',
    ],
    'moveToChild': [
        'NVDA+alt+RightArrow',
        'numpad3',
    ],
    'moveToParent': [
        'NVDA+alt+LeftArrow',
        'numpad7',
    ],
    'moveToPreviousChild': [
        'NVDA+control+alt+RightArrow',
        'numpad9',
    ],
    'moveToNextParent': [
        'NVDA+control+alt+LeftArrow',
        'numpad1',
    ],
    'speakParent': [
        'NVDA+I',
    ],
    'selectSingleIndentationBlock': [
        'NVDA+control+i',
        'control+numpad7',
    ],
    'selectMultipleIndentationBlocks': [
        'NVDA+alt+i',
        'control+numpad9',
    ],
    'speakCurrentLine': [
        'NVDA+Control+l',
        'numpad5',
    ],
    'goBack': [
        'NVDA+control+u',
        'control+numpad1',
    ],
    'goForward': [
        'NVDA+alt+u',
        'control+numpad3',
    ],
}

GC_KEY_MAPS_SOURCE = [
    "review_top",
    "review_previousLine",
    "review_currentLine",
    "review_nextLine",
    "review_bottom",
    "review_previousWord",
    "review_currentWord",
    "review_previousWord",
    "review_nextWord",
    "review_startOfLine",
    "review_previousCharacter",
    "review_currentCharacter",
    "review_nextCharacter",
    "review_endOfLine",
    "reportFocusObjectAccelerator",
]

def normalizeKb(s):
    if s is None:
        return None
    SHIFT_SUFFIX = '+shift'
    if s.endswith(SHIFT_SUFFIX):
        s = s[:-len(SHIFT_SUFFIX)]
        s = "shift+" + s
    return keyboardHandler.KeyboardInputGesture.fromName(s).normalizedIdentifiers[-1]

def makeIndentNavKeyMaps():
    result = {
        k: {}
        for k in IndentNavKeyMap
    }
    for command, keystrokes in IN_KEY_MAPS_SOURCE.items():
        legacyKeystroke = keystrokes[0]
        try:
            numpadKeystroke = keystrokes[1]
        except IndexError:
            numpadKeystroke = keystrokes[0]
        altNumpadKeystroke = 'alt+' + numpadKeystroke
        result[IndentNavKeyMap.LAPTOP][command] = normalizeKb(legacyKeystroke)
        result[IndentNavKeyMap.ALT_NUMPAD][command] = normalizeKb(altNumpadKeystroke)
        result[IndentNavKeyMap.NUMPAD][command] = normalizeKb(numpadKeystroke)
        result[IndentNavKeyMap.NUMPAD_ALT_REVIEW][command] = normalizeKb(numpadKeystroke)
    return result



def makeGlobalCommandsKeyMaps():
    result = {
        k: {}
        for k in IndentNavKeyMap
    }
    for command in GC_KEY_MAPS_SOURCE:
        gestures = [
            g
            for g,c in globalCommands.commands._gestureMap.items()
            if
                "script_" + command == c.__name__
                and g.startswith('kb:')
        ]

        if len(gestures) != 1:
            # weird
            continue
        keystroke = gestures[0].split(':')[1]
        result[IndentNavKeyMap.LAPTOP][command] = normalizeKb(keystroke)
        result[IndentNavKeyMap.ALT_NUMPAD][command] = normalizeKb(keystroke)
        result[IndentNavKeyMap.NUMPAD][command] = normalizeKb(keystroke)
        result[IndentNavKeyMap.NUMPAD_ALT_REVIEW][command] = normalizeKb('alt+' + keystroke)
    return result



def updateKeyMap(cls, keyMap):
    enabled = getConfig("enabled")
    gestures = getattr(cls, f"_{cls.__name__}__gestures")

    gestures = {
        keystroke: script
        for keystroke, script in gestures.items()
        if script not in keyMap
    }
    if enabled:
        gestures = {
            **gestures,
            **{
                gesture: script
                for script, gesture in keyMap.items()
            }
        }
    setattr(cls, f"_{cls.__name__}__gestures", gestures)

def updateIndetnNavKeyMapInObject(obj, keyMap):
    enabled = getConfig("enabled")
    gestures = obj._gestureMap
    functions = {
        getattr(EditableIndentNav, f"script_{script}")
        for script, gesture in keyMap.items()
    }
    gestures = {
        keystroke: script
        for keystroke, script in gestures.items()
        if script.__name__.replace('script_', '') not in keyMap
    }
    if enabled:
        gestures = {
            **gestures,
            **{
                gesture: getattr(EditableIndentNav, f"script_{script}")
                for script, gesture in keyMap.items()
            }
        }
    obj._gestureMap = gestures


def updateKeyMapInObject(ci, keyMap):
    gestures = ci._gestureMap
    gestures = {
        keyMap.get(script.__name__.replace('script_', ''), keystroke): script
        for keystroke, script in gestures.items()
    }
    ci._gestureMap = gestures



IN_KEY_MAPS = makeIndentNavKeyMaps()
GC_KEY_MAPS = makeGlobalCommandsKeyMaps()

def rebindGestures(self):
    # This code is from NVDA's ScriptableObject __init__()
    self._gestureMap = {}
    for cls in reversed(self.__class__.__mro__):
        try:
            self.bindGestures(getattr(cls, "_%s__gestures" % cls.__name__))
        except AttributeError:
            pass
        try:
            self.bindGestures(cls._scriptDecoratorGestures)
        except AttributeError:
            pass

needUpdateGCKeyMap = False
def updateKeyMaps():
    global needUpdateGCKeyMap
    mode = IndentNavKeyMap(getConfig("indentNavKeyMap"))
    if mode == IndentNavKeyMap.NUMPAD_ALT_REVIEW:
        needUpdateGCKeyMap = True
    keyMap = IN_KEY_MAPS[mode]
    updateKeyMap(EditableIndentNav, keyMap)
    if needUpdateGCKeyMap:
        updateKeyMapInObject(globalCommands.commands, GC_KEY_MAPS[mode])
        try:
            ci = next(gp for gp in globalPluginHandler.runningPlugins if gp.__module__ == 'globalPlugins.charinfo')
            updateKeyMapInObject(ci, GC_KEY_MAPS[mode])
        except StopIteration:
            pass
    focus = api.getFocusObject()
    rebindGestures(focus)


config.post_configProfileSwitch .register(updateKeyMaps)


def initConfiguration():
    clutterRegex = (
        r"^\s*(" +
        "|".join([
          # Python
            # ) : #comment
                r"\)\s*:?\s*(#.*)?",
            # ) -> type :
                r"""\)\s*->[\s\w.,\[\]|"']*:""",
            # ), # comment
            # ], # comment
            # }, # comment
            # Also allows // comment; also allows semicolon;
                r"[\])}]\s*[,;]?\s*((#|//).*)?",
            # { // comment
                r"[{]\s*((#|//).*)?",
            # # comment
                r"#.*",
            # from? import
                r"(^from\s+[\w\s.]+\s+|^)import\s+.*",
          # C++
            # ) { // comment
                r"\)\s*[{;]?\s*(//.*)?",
            # // comment
                r"//.*",
            # #include
                r"^#include.*",
        ])
        + r")\s*$"
    )
    defaultQuickFind = json.dumps({
        'bookmarks': []
    }).replace("'", r"\'")
    confspec = {
        "crackleVolume" : "integer( default=25, min=0, max=100)",
        "noNextTextChimeVolume" : "integer( default=50, min=0, max=100)",
        "noNextTextMessage" : "boolean( default=False)",
        "legacyVSCode" : "boolean( default=False)",
        "indentNavKeyMap" : "integer( default=1, min=0, max=3)",
        "clutterRegex" : f"string( default='{clutterRegex}')",
        "quickFind" : f"string( default='{defaultQuickFind}')",
        "enabled" : "boolean( default=True)",
    }
    config.conf.spec["indentnav"] = confspec

def getConfig(key):
    value = config.conf["indentnav"][key]
    return value

def setConfig(key, value):
    config.conf["indentnav"][key] = value


addonHandler.initTranslation()
initConfiguration()

@dataclasses.dataclass
class QuickFindBookmark:
    name: str
    keystroke: str
    pattern: str
    enabled: bool = True

    def getDisplayName(self):
        return self.name or self.keystroke

def loadBookmarks():
    items = json.loads(getConfig("quickFind"))['bookmarks']
    items = [QuickFindBookmark(**item) for item in items]
    return items

def saveBookmarks(bookmarks):
   items = [dataclasses.asdict(item) for item in bookmarks]
   setConfig("quickFind", json.dumps({
        'bookmarks': items,
    }))

globalBookmarks = {}
def reloadBookmarks():
    global globalBookmarks
    bookmarks = loadBookmarks()
    globalBookmarks = {
        bookmark.keystroke: bookmark
        for bookmark in bookmarks
    }
    cls = EditableIndentNav
    gestures = getattr(cls, f"_{cls.__name__}__gestures")
    QF = "quickFind"
    gestures = {
        keystroke: script
        for keystroke, script in gestures.items()
        if script != QF
    }
    gestures = {
        **gestures,
        **{
            keyboardHandler.KeyboardInputGesture.fromName(keystroke).normalizedIdentifiers[-1]: QF
            for keystroke, bookmark in globalBookmarks.items()
            if bookmark.enabled
        },
        **{
            keyboardHandler.KeyboardInputGesture.fromName("shift+" + keystroke).normalizedIdentifiers[-1]: QF
            for keystroke, bookmark in globalBookmarks.items()
            if bookmark.enabled
        },
    }
    setattr(cls, f"_{cls.__name__}__gestures", gestures)



def getKeystrokeFromGesture(gesture):
    #keystroke = gesture.normalizedIdentifiers[-1].split(':')[1]
    keystroke = gesture.identifiers[-1].split(':')[1]
    return keystroke


class SettingsDialog(SettingsPanel):
    # Translators: Title for the settings dialog
    title = _("IndentNav settings")


    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

    def makeSettings(self, settingsSizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
      # Key map combo box
        label = _("Keyboard shortcuts")
        self.keyMapComboBox = sHelper.addLabeledControl(
            label,
            wx.Choice,
            choices=[mode.displayString for mode in IndentNavKeyMap]
        )
        index = getConfig("indentNavKeyMap")
        self.keyMapComboBox.SetSelection(index)
      # Checkbox enabled
        label = _("Enable IndentNav")
        self.enabledCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.enabledCheckbox.Value = getConfig("enabled")
      # crackleVolumeSlider
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        # Translators: volume of crackling slider
        label=wx.StaticText(self,wx.ID_ANY,label=_("Crackling volume"))
        slider=wx.Slider(self, wx.NewId(), minValue=0,maxValue=100)
        slider.SetValue(getConfig("crackleVolume"))
        sizer.Add(label)
        sizer.Add(slider)
        settingsSizer.Add(sizer)
        self.crackleVolumeSlider = slider

      # noNextTextChimeVolumeSlider
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        # Translators: End of document chime volume
        label=wx.StaticText(self,wx.ID_ANY,label=_("Volume of chime when no more sentences available"))
        slider=wx.Slider(self, wx.NewId(), minValue=0,maxValue=100)
        slider.SetValue(getConfig("noNextTextChimeVolume"))
        sizer.Add(label)
        sizer.Add(slider)
        settingsSizer.Add(sizer)
        self.noNextTextChimeVolumeSlider = slider

      # Checkboxes noNextTextMessageCheckbox
        # Translators: Checkbox that controls spoken message when no next or previous text paragraph is available in the document
        label = _("Speak message when no next paragraph containing text available in the document")
        self.noNextTextMessageCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.noNextTextMessageCheckbox.Value = getConfig("noNextTextMessage")
      # EditBox clutter regexp
        label = _("Clutter regular expression")
        self.clutterRegexEdit = sHelper.addLabeledControl(label, wx.TextCtrl)
        self.clutterRegexEdit.Value = getConfig("clutterRegex")

      # Checkboxes legacy VSCode
        label = _("Use legacy mode in VSCode (not recommended)")
        self.legacyVSCodeCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.legacyVSCodeCheckbox.Value = getConfig("legacyVSCode")
      # Install VSCode extension button
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        item = self.installButton = wx.Button(self, label=_("&Install VSCode extension (recommended)"))
        item.Bind(wx.EVT_BUTTON, self.onInstall)
        sizer.Add(item)
      # Learn about VSCode Extension
        item = self.learnButton = wx.Button(self, label=_("&Learn more about VSCode accessibility extension"))
        item.Bind(wx.EVT_BUTTON, self.onLearn)
        sizer.Add(item)
        settingsSizer.Add(sizer)

    def onInstall(self, evt):
        msg = _(
            "We will install accessibility extension in default VSCode instance on your system - the one found in %PATH% environment variable.\n"
            "If you have multiple instances or a custom version of VSCode, such as VSCode Insiders, you would need to install accessibility extension manually.\n"
            "Please review output of command to make sure installation is successful.\n"
            "If successful, the extension would be launched right away and there is no need to restart VSCode.\n"
            "Are you sure you want to proceed?"
        )
        dlg = wx.MessageDialog(None, msg, _("Confirmation"), wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            installVSCodeExtension()

    def onLearn(self, evt):
        url = "https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility"
        os.startfile(url)
        
    def isValid(self) -> bool:
        clutterRegex = self.clutterRegexEdit.Value
        try:
            re.compile(clutterRegex)
        except re.error as e:
            errorMsg = _('Failed to compile regular expression: %s') % str(e)
            gui.messageBox(errorMsg, _("Regular expression error"), wx.OK|wx.ICON_WARNING, self)
            #self.clutterRegexEdit.SetFocus()
            return False
        return True



    def onSave(self):
        clutterRegex = self.clutterRegexEdit.Value
        setConfig("clutterRegex", clutterRegex)
        config.conf["indentnav"]["indentNavKeyMap"] = self.keyMapComboBox.GetSelection()
        config.conf["indentnav"]["enabled"] = self.enabledCheckbox.Value
        config.conf["indentnav"]["crackleVolume"] = self.crackleVolumeSlider.Value
        config.conf["indentnav"]["noNextTextChimeVolume"] = self.noNextTextChimeVolumeSlider.Value
        config.conf["indentnav"]["noNextTextMessage"] = self.noNextTextMessageCheckbox.Value
        config.conf["indentnav"]["legacyVSCode"] = self.legacyVSCodeCheckbox.Value
        updateKeyMaps()


class EditBookmarkDialog(wx.Dialog):
    def __init__(self, parent, bookmark=None):
        title=_("Edit IndentNav QuickFind bookmark")
        super(EditBookmarkDialog,self).__init__(parent,title=title)
        mainSizer=wx.BoxSizer(wx.VERTICAL)
        sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
        if bookmark is  not None:
            self.bookmark = bookmark
        else:
            self.bookmark = QuickFindBookmark(
                name="",
                keystroke="",
                pattern="",
            )
        self.keystroke = self.bookmark.keystroke
      # Translators: label for name
        commentLabelText = _("&Display name (optional)")
        self.commentTextCtrl=sHelper.addLabeledControl(commentLabelText, wx.TextCtrl)
        self.commentTextCtrl.SetValue(self.bookmark.name)
      # Translators:  Custom keystroke button
        self.customeKeystrokeButton = sHelper.addItem (wx.Button (self, label = _("&Keystroke")))
        self.customeKeystrokeButton.Bind(wx.EVT_BUTTON, self.OnCustomKeystrokeClick)
        self.updateCustomKeystrokeButtonLabel()

      # Translators: pattern
        patternLabelText = _("&Pattern")
        self.patternTextCtrl=sHelper.addLabeledControl(patternLabelText, wx.TextCtrl)
        self.patternTextCtrl.SetValue(self.bookmark.pattern)
      # Translators: label for enabled checkbox
        enabledText = _("Bookmark enabled")
        self.enabledCheckBox=sHelper.addItem(wx.CheckBox(self,label=enabledText))
        self.enabledCheckBox.SetValue(self.bookmark.enabled)
      #  OK/cancel buttons
        sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK|wx.CANCEL))

        mainSizer.Add(sHelper.sizer,border=20,flag=wx.ALL)
        mainSizer.Fit(self)
        self.SetSizer(mainSizer)
        self.commentTextCtrl.SetFocus()
        self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)

    def make(self, snippet=None, quiet=False):
        pattern = self.patternTextCtrl.Value
        pattern = pattern.rstrip("\r\n")
        errorMsg = None
        if len(pattern) == 0:
            errorMsg = _('Pattern cannot be empty!')
        else:
            try:
                re.compile(pattern)
            except re.error as e:
                errorMsg = _('Failed to compile regular expression: %s') % str(e)

        if errorMsg is not None:
            # Translators: This is an error message to let the user know that the pattern field is not valid.
            gui.messageBox(errorMsg, _("Bookmark entry error"), wx.OK|wx.ICON_WARNING, self)
            self.patternTextCtrl.SetFocus()
            return

        if len(self.keystroke) == 0:
            errorMsg = _("Please specify keystroke gesture.")
            gui.messageBox(errorMsg, _("Bookmark entry error"), wx.OK|wx.ICON_WARNING, self)
            self.customeKeystrokeButton.SetFocus()
            return
        bookmark = QuickFindBookmark(
            enabled=self.enabledCheckBox.Value,
            name=self.commentTextCtrl.Value,
            pattern=pattern,
            keystroke=self.keystroke,
        )
        return bookmark

    def updateCustomKeystrokeButtonLabel(self):
        keystroke = self.keystroke
        if keystroke:
            self.customeKeystrokeButton.SetLabel(_("&Keystroke: %s") % (keystroke))
        else:
            self.customeKeystrokeButton.SetLabel(_("Keystroke: None"))

    def OnCustomKeystrokeClick(self,evt):
        if inputCore.manager._captureFunc:
            # don't add while already in process of adding.
            return
        def addGestureCaptor(gesture: inputCore.InputGesture):
            if gesture.isModifier:
                return False
            inputCore.manager._captureFunc = None
            wx.CallAfter(self._addCaptured, gesture)
            return False
        inputCore.manager._captureFunc = addGestureCaptor
        core.callLater(50, ui.message, _("Press desired keystroke now"))

    blackListedKeystrokes = "escape enter numpadenter space nvda+space nvda+n nvda+q nvda+j j tab uparrow downarrow leftarrow rightarrow home end control+home control+end delete".split()

    def _addCaptured(self, gesture):
        g = getKeystrokeFromGesture(gesture)
        if g  in self.blackListedKeystrokes:
            msg = _("Invalid keystroke %s: cannot overload essential  NVDA keystrokes!") % g
        elif 'shift+' in g:
            msg = _("Invalid keystroke %s: Cannot use keystrokes with shift modifier for quickFind bookmarks!") % g
        else:
            self.keystroke = g
            msg = None
        if msg:
            core.callLater(50, ui.message, msg)
        self.updateCustomKeystrokeButtonLabel()

    def onOk(self,evt):
        bookmark = self.make()
        if bookmark is not None:
                self.bookmark = bookmark
                evt.Skip()


class QuickFindSettingsDialog(SettingsPanel):
    # Translators: Title for the settings dialog
    title = _("IndentNav QuickFind bookmarks settings")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def makeSettings(self, settingsSizer):
        self.bookmarks = loadBookmarks()
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
      # bookmarks table
        label = _("&QuickFind bookmarks")
        self.bookmarksList = sHelper.addLabeledControl(
            label,
            nvdaControls.AutoWidthColumnListCtrl,
            autoSizeColumn=2,
            itemTextCallable=self.getItemTextForList,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VIRTUAL
        )

        self.bookmarksList.InsertColumn(0, _("Name"), width=self.scaleSize(150))
        self.bookmarksList.InsertColumn(1, _("Enabled"), width=self.scaleSize(150))
        self.bookmarksList.InsertColumn(2, _("Gesture"))
        self.bookmarksList.InsertColumn(3, _("Pattern"))
        self.bookmarksList.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onListItemFocused)
        self.bookmarksList.ItemCount = len(self.bookmarks)

        bHelper = sHelper.addItem(guiHelper.ButtonHelper(orientation=wx.HORIZONTAL))
      # Buttons
        self.addButton = bHelper.addButton(self, label=_("&Add"))
        self.addButton.Bind(wx.EVT_BUTTON, self.OnAddClick)
        self.editButton = bHelper.addButton(self, label=_("&Edit"))
        self.editButton.Bind(wx.EVT_BUTTON, self.OnEditClick)
        self.removeButton = bHelper.addButton(self, label=_("&Remove"))
        self.removeButton.Bind(wx.EVT_BUTTON, self.OnRemoveClick)
        self.moveUpButton = bHelper.addButton(self, label=_("Move &up"))
        self.moveUpButton.Bind(wx.EVT_BUTTON, lambda evt: self.OnMoveClick(evt, -1))
        self.moveDownButton = bHelper.addButton(self, label=_("Move &down"))
        self.moveDownButton.Bind(wx.EVT_BUTTON, lambda evt: self.OnMoveClick(evt, 1))
        self.sortButton = bHelper.addButton(self, label=_("&Sort"))
        self.sortButton.Bind(wx.EVT_BUTTON, self.OnSortClick)

    def getItemTextForList(self, item, column):
        bookmark = self.bookmarks[item]
        if column == 0:
            return bookmark.name or bookmark.keystroke
        elif column == 1:
            return _("Enabled") if bookmark.enabled else _("Disabled")
        elif column == 2:
            return bookmark.keystroke
        elif column == 3:
            return bookmark.pattern
        else:
            raise ValueError("Unknown column: %d" % column)

    def onListItemFocused(self, evt):
        if self.bookmarksList.GetSelectedItemCount()!=1:
            return
        index=self.bookmarksList.GetFirstSelected()
        bookmark = self.bookmarks[index]

    def OnAddClick(self,evt):
        entryDialog=EditBookmarkDialog(self)
        if entryDialog.ShowModal()==wx.ID_OK:
            bookmarks = list(self.bookmarks) + [entryDialog.bookmark]
            self.bookmarks = bookmarks
            self.bookmarksList.ItemCount = len(self.bookmarks)
            index = self.bookmarksList.ItemCount - 1
            self.bookmarksList.Select(index)
            self.bookmarksList.Focus(index)
            # We don't get a new focus event with the new index.
            self.bookmarksList.sendListItemFocusedEvent(index)
            self.bookmarksList.SetFocus()
            entryDialog.Destroy()

    def OnEditClick(self,evt):
        if self.bookmarksList.GetSelectedItemCount()!=1:
            return
        editIndex=self.bookmarksList.GetFirstSelected()
        if editIndex<0:
            return
        entryDialog=EditBookmarkDialog(
            self,
            self.bookmarks[editIndex],
        )
        if entryDialog.ShowModal()==wx.ID_OK:
            self.bookmarks[editIndex] = entryDialog.bookmark
            self.bookmarksList.SetFocus()
        entryDialog.Destroy()

    def OnRemoveClick(self,evt):
        bookmarks = list(self.bookmarks)
        index=self.bookmarksList.GetFirstSelected()
        while index>=0:
            self.bookmarksList.DeleteItem(index)
            del bookmarks[index]
            index=self.bookmarksList.GetNextSelected(index)
        self.bookmarksList.SetFocus()

    def OnMoveClick(self,evt, increment):
        if self.bookmarksList.GetSelectedItemCount()!=1:
            return
        index=self.bookmarksList.GetFirstSelected()
        if index<0:
            return
        newIndex = index + increment
        if 0 <= newIndex < len(self.bookmarks):
            bookmarks = list(self.bookmarks)
            # Swap
            tmp = bookmarks[index]
            bookmarks[index] = bookmarks[newIndex]
            bookmarks[newIndex] = tmp
            self.bookmarks = bookmarks
            self.bookmarksList.Select(newIndex)
            self.bookmarksList.Focus(newIndex)
        else:
            return

    def OnSortClick(self,evt):
        bookmarks = list(self.bookmarks)
        bookmarks.sort(key=QuickFindBookmark.getDisplayName)
        self.bookmarks = bookmarks

    def onSave(self):
        saveBookmarks(self.bookmarks)
        reloadBookmarks()

original_reportExtra = None
def my_reportExtra(self):
    # we only report numLock if no modifiers are pressed
    if len(self.modifiers) == 0:
        return original_reportExtra(self)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("IndentNav")
    def __init__(self, *args, **kwargs):
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        self.createMenu()
        self.injectHooks()
        updateKeyMaps()
        # Also wait 1 second until all add-ons are loaded before updating keymap again to deal with charInfo add-on
        core.callLater(500, updateKeyMaps)
        reloadBookmarks()


    def terminate(self):
        self.restoreHooks()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SettingsDialog)
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(QuickFindSettingsDialog)

    def createMenu(self):
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SettingsDialog)
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(QuickFindSettingsDialog)

    def injectHooks(self):
        global original_reportExtra
        original_reportExtra = keyboardHandler.KeyboardInputGesture.reportExtra
        keyboardHandler.KeyboardInputGesture.reportExtra = my_reportExtra

    def restoreHooks(self):
        global original_reportExtra
        keyboardHandler.KeyboardInputGesture.reportExtra = original_reportExtra


    def chooseNVDAObjectOverlayClasses (self, obj, clsList):
        try:
            obj.windowClassName
        except AttributeError:
            return
        if obj.windowClassName == u'Scintilla':
            clsList.append(EditableIndentNav)
            return
        if obj.windowClassName == u"AkelEditW":
            clsList.append(EditableIndentNav)
            return
        if obj.windowClassName == u"RichEditD2DPT":
            clsList.append(EditableIndentNav)
            return
        if obj.role == ROLE_EDITABLETEXT:
            clsList.append(EditableIndentNav)
            return

    @script(description=_("Toggle IndentNav"), gestures=['kb:alt+numLock'])
    def script_toggleIndentNav(self, gesture):
        focus = api.getFocusObject()
        if not isinstance(focus, EditableIndentNav):
            focus = None
        toggleState = winUser.getKeyState(gesture.vkCode) & 1
        if toggleState:
            ui.message(_("Please turn off num lock in order to toggle IndentNav"))
            return
        if gesture.mainKeyName == 'numLock':
            # Something wrong happens with num lock state, where NVDA reports is as not changed, whereas Windows treats it as changed. This is the workaround:
            nl = keyboardHandler.KeyboardInputGesture.fromName("numLock")
            nl.send()
            nl.send()
        enabled = getConfig("enabled")
        enabled = not enabled
        setConfig("enabled", enabled)
        if enabled:
            msg = _("Enabled IndentNav")
        else:
            msg = _("Disabled IndentNav")
        ui.message(msg)
        updateKeyMaps()



class Beeper:
    BASE_FREQ = speech.IDT_BASE_FREQUENCY
    def getPitch(self, indent):
        return self.BASE_FREQ*2**(indent/24.0) #24 quarter tones per octave.

    BEEP_LEN = 10 # millis
    PAUSE_LEN = 5 # millis
    MAX_CRACKLE_LEN = 400 # millis
    MAX_BEEP_COUNT = MAX_CRACKLE_LEN // (BEEP_LEN + PAUSE_LEN)


    def fancyCrackle(self, levels, volume):
        levels = self.uniformSample(levels, self.MAX_BEEP_COUNT )
        beepLen = self.BEEP_LEN
        pauseLen = self.PAUSE_LEN
        pauseBufSize = NVDAHelper.generateBeep(None,self.BASE_FREQ,pauseLen,0, 0)
        beepBufSizes = [NVDAHelper.generateBeep(None,self.getPitch(l), beepLen, volume, volume) for l in levels]
        bufSize = sum(beepBufSizes) + len(levels) * pauseBufSize
        buf = ctypes.create_string_buffer(bufSize)
        bufPtr = 0
        for l in levels:
            bufPtr += NVDAHelper.generateBeep(
                ctypes.cast(ctypes.byref(buf, bufPtr), ctypes.POINTER(ctypes.c_char)),
                self.getPitch(l), beepLen, volume, volume)
            bufPtr += pauseBufSize # add a short pause
        tones.player.stop()
        tones.player.feed(buf.raw)

    def simpleCrackle(self, n, volume):
        return self.fancyCrackle([0] * n, volume)


    NOTES = "A,B,H,C,C#,D,D#,E,F,F#,G,G#".split(",")
    NOTE_RE = re.compile("[A-H][#]?")
    BASE_FREQ = 220
    def getChordFrequencies(self, chord):
        myAssert(len(self.NOTES) == 12)
        prev = -1
        result = []
        for m in self.NOTE_RE.finditer(chord):
            s = m.group()
            i =self.NOTES.index(s)
            while i < prev:
                i += 12
            result.append(int(self.BASE_FREQ * (2 ** (i / 12.0))))
            prev = i
        return result

    def fancyBeep(self, chord, length, left=10, right=10):
        beepLen = length
        freqs = self.getChordFrequencies(chord)
        intSize = 8 # bytes
        bufSize = max([NVDAHelper.generateBeep(None,freq, beepLen, right, left) for freq in freqs])
        if bufSize % intSize != 0:
            bufSize += intSize
            bufSize -= (bufSize % intSize)
        tones.player.stop()
        bbs = []
        result = [0] * (bufSize//intSize)
        for freq in freqs:
            buf = ctypes.create_string_buffer(bufSize)
            NVDAHelper.generateBeep(buf, freq, beepLen, right, left)
            bytes = bytearray(buf)
            unpacked = struct.unpack("<%dQ" % (bufSize // intSize), bytes)
            result = map(operator.add, result, unpacked)
        maxInt = 1 << (8 * intSize)
        result = map(lambda x : x %maxInt, result)
        packed = struct.pack("<%dQ" % (bufSize // intSize), *result)
        tones.player.feed(packed)

    def uniformSample(self, a, m):
        n = len(a)
        if n <= m:
            return a
        # Here assume n > m
        result = []
        for i in range(0, m*n, n):
            result.append(a[i // m])
        return result


class TextInfoUnavailableException(Exception):
    pass

class VSCodeNotMainEditorException(Exception):
    pass


class FastLineManagerV2:
    def __init__(self, obj, selectionMode=False):
        self.obj = obj
        self.selectionMode = selectionMode

    def __enter__(self):
        legacyVSCode = getConfig("legacyVSCode")
        document = self.obj.makeEnhancedTextInfo(textInfos.POSITION_ALL, allowPlainTextInfoInVSCode=legacyVSCode)
        if not self.selectionMode:
            self.originalCaret = self.obj.makeEnhancedTextInfo(textInfos.POSITION_CARET, allowPlainTextInfoInVSCode=legacyVSCode)
        else:
            self.originalSelection = self.obj.makeEnhancedTextInfo(textInfos.POSITION_SELECTION, allowPlainTextInfoInVSCode=legacyVSCode)
            self.originalCaret = self.originalSelection.copy()
            self.originalCaret.collapse()
        if document is None or  self.originalCaret is None:
            raise TextInfoUnavailableException
        pretext = self.originalCaret.copy()
        pretext.collapse()
        pretext.setEndPoint(document, "startToStart")
        self.lineIndex = len(self.splitlines(pretext.text)[0]) - 1
        self.originalLineIndex = self.lineIndex
        self.lines, self.offsets = self.splitlines(document.text)
        self.nLines = len(self.lines)
        self.originalCaret.expand(textInfos.UNIT_LINE)
        self.document = document
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def move(self, increment):
        newIndex = self.lineIndex + increment
        if (newIndex < 0) or (newIndex >= self.nLines):
            return 0
        self.lineIndex = newIndex
        return increment

    def getText(self):
        return self.lines[self.lineIndex]

    def getLine(self):
        return self.lineIndex

    def updateCaret(self, line):
        line = self.getTextInfo(line)
        caret = line.copy()
        caret.collapse()
        caret.updateCaret()
        return line

    def getLineUnit(self):
        if isinstance(self.originalCaret, VsWpfTextViewTextInfo):
            # TextInfo in Visual Studio doesn't understand UNIT_PARAGRAPH
            return textInfos.UNIT_LINE
        # In Windows 11 Notepad, we should use UNIT_PARAGRAPH instead of UNIT_LINE in order to handle wrapped lines correctly
        return textInfos.UNIT_PARAGRAPH

    def getTextInfo(self, line=None):
        if line is None:
            line = self.lineIndex
        textInfo = self.document.copy()
        compoundMode = False
        if isinstance(textInfo, CompoundTextInfo):
            if textInfo._start == textInfo._end and  isinstance(textInfo._start, OffsetsTextInfo):
                compoundMode = True
                outerTextInfo = textInfo
                textInfo = outerTextInfo._start
        if isinstance(textInfo, OffsetsTextInfo):
            encoding = textInfo.encoding
            converter = textUtils.getOffsetConverter(encoding)(self.document.text)
            nativeOffset = converter.strToEncodedOffsets(self.offsets[line])
            textInfo._startOffset = textInfo._endOffset = nativeOffset
            textInfo.expand(textInfos.UNIT_LINE)
        else:
            unit = self.getLineUnit()
            delta = line - self.originalLineIndex
            textInfo = self.originalCaret.copy()
            textInfo.expand(unit)
            textInfo.collapse()
            result = textInfo.move(unit, delta)
            if result != delta:
                raise Exception(f"Failed to move by {delta} lines")
            textInfo.expand(textInfos.UNIT_LINE)
            return textInfo
        if compoundMode:
            outerTextInfo = outerTextInfo.copy()
            outerTextInfo._start = outerTextInfo._end = textInfo
            return outerTextInfo
        return textInfo

    NEWLINE_REGEX = re.compile(r"\r?\n|\r", )
    def splitlines(self, s):
        lines = []
        offsets = [0]
        for m in  self.NEWLINE_REGEX.finditer(s):
            lines.append(s[offsets[-1]:m.start(0)])
            offsets.append(m.end(0))
        lines.append(s[offsets[-1]:])
        return lines, offsets

def installVSCodeExtension():
    cmd = f'cmd /k code --install-extension TonyMalykh.nvda-indent-nav-accessibility'
    def doInstall():
        os.system(cmd)

    threading.Thread(
        name="IndentNav VSCode extension installer thread",
        target=doInstall,
    ).start()


namedPipesCache = {}
HWND_TO_PID = {}
@dataclasses.dataclass
class PiperRequest:
    request: dict = None
    shutdownRequested: bool = False
    outputQueue: queue.Queue = None

@dataclasses.dataclass
class PiperResponse:
    pid: int
    response: dict


class VSCodePiper(threading.Thread):
    def __init__(self, pid):
        super().__init__(name=f"IndentNav Piper thread for pid={pid}")
        self.pid = pid
        pipeName = r"\\.\pipe\VSCodeIndentNavBridge" + str(pid)
        #log.error(f"asdf {pipeName}")
        self.f = open(pipeName, 'rb+', buffering=0)
        self.inputQueue  = queue.Queue()
        self.closed = False
        self.start()


    def run(self):
        buffer = b''
        CHUNK = 2**20
        messageLength = -1
        while not self.closed:
            request = self.inputQueue.get(True)
            if request.shutdownRequested:
                self.closed = True
                return
            while True:
                messageBytes = self.f.read(CHUNK)
                if not messageBytes:
                    self.closed = True
                    request.outputQueue.put(PiperResponse(
                        pid=self.pid,
                        response={
                            "error": f"Named pipe for pid={pid} closed unexpectedly",
                        },
                    ))
                    return
                #log.error(f"asdf received {len(messageBytes)} bytes")
                buffer += messageBytes
                if messageLength == -1 and len(buffer) >= 4:
                    messageLength = struct.unpack('I', buffer[:4])[0]
                    buffer = buffer[4:]
                    #log.error(f"asdf len={messageLength}")
                if messageLength != -1 and len(buffer) >= messageLength:
                    s = buffer[:messageLength].decode('utf-8')
                    buffer = buffer[messageLength:]
                    messageLength = -1
                    try:
                        response = json.loads(s)
                    except json.decoder.JSONDecodeError as e:
                        response = {
                            'error': str(e)
                        }
                    request.outputQueue.put(PiperResponse(
                        pid=self.pid,
                        response=response,
                    ))
                    break

    def get(self):
        TIMEOUT = 1 #second
        q = queue.Queue()
        self.inputQueue.put(PiperRequest(
            outputQueue=q,
        ))
        try:
            response = q.get(timeout=TIMEOUT)
        except queue.Empty as e:
            self.closed = True
            raise RuntimeError("Named pipe communication timeout", e)
        message = response.response
        return message

    def send(self, j):
        s = json.dumps(j)
        b = s.encode('utf-8')
        message = struct.pack('I', len(b)) + b
        self.f.write(message)

    def callImpl(self, request):
        if self.closed:
            raise RuntimeError("This piper is closed")
        self.send(request)
        return self.get()

    def call(self, command, **kwargs):
        result = self.callImpl({
            **{"command": command},
            **kwargs,
        })
        try:
            return result["result"]
        except KeyError:
            raise RuntimeError(f"VSCode accessibility extension raised error: {result['error']}")

    def callImplSpecial(self, request, queue):
        if self.closed:
            raise RuntimeError("This piper is closed")
        self.send(request)
        self.inputQueue.put(PiperRequest(
            outputQueue=queue,
        ))


    def join(self):
        """
            Your head is humming, and it won't go, in case you don't know
            The piper's calling you to join him!
        """
        self.inputQueue.put(PiperRequest(
            shutdownRequested=True,
        ))
        if not self.closed:
            super().join()

    def getStoryLength(self):
        return self.call("getStoryLength")

    def getStoryText(self):
        return self.call("getStoryText")

    def getCaretOffset(self):
        return self.call("getCaretOffset")

    def setCaretOffset(self, offset):
        return self.call("setCaretOffset", offset=offset)

    def getSelectionOffsets(self):
        result = self.call("getSelectionOffsets")
        return [min(result), max(result)]

    def setSelectionOffsets(self, anchorOffset, caretOffset):
        return self.call("setSelectionOffsets", anchorOffset=anchorOffset, offset=caretOffset)

    def getStatus(self):
        return self.call("getStatus")


def updatePipers():
    global namedPipesCache
    PIPE_DIR = r"\\.\pipe"
    PIPE_PREFIX = "VSCodeIndentNavBridge"
    piperPids = []
    for s in os.listdir(PIPE_DIR):
        if s.startswith(PIPE_PREFIX):
            try:
                pid = int(s[len(PIPE_PREFIX):])
            except ValueError:
                continue
            piperPids.append(pid)
    #log.error(f"asdf piperPids={piperPids}")
    pidsToRemove = []
    for pid, piper in namedPipesCache.items():
        if pid not in piperPids or piper.closed:
            piper.join()
            pidsToRemove.append(pid)
            #log.error(f"asdf Killing piper for pid={pid}")
    namedPipesCache = {k: v for k, v in namedPipesCache.items() if k in pidsToRemove}
    #log.error(f"asdf namedPipesCache={list(namedPipesCache.keys())}")
    for pid in [pid for pid in piperPids if pid not in namedPipesCache]:
        #log.error(f"asdf opening piper for pid={pid}")
        try:
            namedPipesCache[pid] = VSCodePiper(pid)
        except FileNotFoundError:
            continue

def findActivePiper():
    q = queue.Queue()
    request = {
        "command": "getStatus",
    }
    n = 0
    for pid, piper in namedPipesCache.items():
        if piper.closed:
            continue
        try:
            piper.callImplSpecial(request, q)
            n += 1
        except Exception:
            log.exception(f"Piper callImplSpecial exception for pid={pid}")
    t0 = time.time()
    TIMEOUT = 1 #second
    t1 = t0 + TIMEOUT
    while n > 0:
        waitTime = t1 - time.time()
        if waitTime <= 0:
            break
        try:
            response = q.get(True, waitTime)
            n -= 1
            #log.error(f"asdf {response.response}")
            if response.response["result"]["focused"]:
                return response.pid
        except queue.Empty:
            break
        except KeyError:
            log.warning(f"getStatus called failed with error: {response.response}")
    return None

def getPiperForFocus():
    global HWND_TO_PID
    focus = api.getFocusObject()
    hwnd = focus.windowHandle
    try:
        piperPid =HWND_TO_PID[hwnd]
        piper = namedPipesCache[piperPid]
        return piper
    except KeyError:
        pass
    updatePipers()
    piperPid = findActivePiper()
    if piperPid is not None:
        HWND_TO_PID[hwnd] = piperPid
        piper = namedPipesCache[piperPid]
        return piper
    return None



class VSCodeTextInfo(NVDAObjectTextInfo):
    encoding = textUtils.WCHAR_ENCODING # empirically verified

    def __init__(self,obj,position):
        obj = obj or position.obj
        self.piper = obj.piper
        #self.strongObj = obj # to prevent obj from being gc'd
        super().__init__(obj, position)

    def _getStoryLength(self):
        return self.piper.getStoryLength()

    def _getStoryText(self):
        return self.piper.getStoryText()

    def _getCaretOffset(self):
        return self.piper.getCaretOffset()

    def updateCaret(self):
        self.piper.setCaretOffset(self._startOffset)

    def _getSelectionOffsets(self):
        return self.piper.getSelectionOffsets()
    def updateSelection(self):
        self.piper.setSelectionOffsets(self._startOffset, self._endOffset)

    def copy(self):
        return VSCodeTextInfo(None, self)


class VSCodeRequestDialog(wx.Dialog):
    MESSAGE = _(
        "IndentNav requires VSCode accessibility extension to be installed in order to work correctly in VSCode."
    )

    def __init__(self, parent, appModule):
        super().__init__(parent, title=_("Please install VSCode extension"))
        self.appModule = appModule
        mainSizer=wx.BoxSizer(wx.VERTICAL)
        item = wx.StaticText(self, label=self.MESSAGE)
        mainSizer.Add(item, border=20, flag=wx.LEFT | wx.RIGHT | wx.TOP)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        item = self.installButton = wx.Button(self, label=_("&Install VSCode extension (recommended)"))
        item.Bind(wx.EVT_BUTTON, self.onInstall)
        sizer.Add(item)
        item = self.learnButton = wx.Button(self, label=_("&Learn more about VSCode accessibility extension"))
        item.Bind(wx.EVT_BUTTON, self.onLearn)
        sizer.Add(item)
        item = self.legacyButton = wx.Button(self, label=_("&Use VSCode in legacy mode without extension (not recommended)"))
        item.Bind(wx.EVT_BUTTON, self.onLegacy)
        sizer.Add(item)
        item = wx.Button(self, wx.ID_CLOSE, label=_("&Cancel"))
        item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
        sizer.Add(item)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.EscapeId = wx.ID_CLOSE
        mainSizer.Add(sizer, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=20)

        self.Sizer = mainSizer
        mainSizer.Fit(self)
        self.CentreOnScreen()
        self.Show()
        self.Raise()
        self.SetFocus()

    def onInstall(self, evt):
        msg = _(
            "We will install accessibility extension in default VSCode instance on your system - the one found in %PATH% environment variable.\n"
            "If you have multiple instances or a custom version of VSCode, such as VSCode Insiders, you would need to install accessibility extension manually.\n"
            "Please review output of command to make sure installation is successful.\n"
            "If successful, the extension would be launched right away and there is no need to restart VSCode.\n"
            "Are you sure you want to proceed?"
        )
        dlg = wx.MessageDialog(None, msg, _("Confirmation"), wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.onClose(None)
            installVSCodeExtension()

    def onLearn(self, evt):
        url = "https://marketplace.visualstudio.com/items?itemName=TonyMalykh.nvda-indent-nav-accessibility"
        os.startfile(url)
        self.onClose(None)

    def onLegacy(self, evt):
        msg = _(
            "Please enable legacy support of VSCode in IndentNav settings.\n"
            "Please note that builtin VSCode accessibility provides access to only 500 lines of code.\n"
            "As a result, in larger files IndentNav will not work correctly.\n"
            "Please use it at your own risk."
        )
        wx.MessageBox(msg, _('Information'), wx.OK | wx.ICON_INFORMATION)
        self.onClose(None)


    def onClose(self, evt):
        self.Hide()

def isVSCodeMainEditor(obj):
    if obj.role != controlTypes.Role.EDITABLETEXT:
        return False
    def findLandmark(obj):
        simpleParent = obj.simpleParent
        if simpleParent.role == controlTypes.Role.LANDMARK:
            return simpleParent
        while True:
            obj = obj.parent
            if obj is None:
                return None
            if obj.role == controlTypes.Role.LANDMARK:
                return obj

    landmark = findLandmark(obj)
    if landmark is None:
        return False
    try:
        return landmark.IA2Attributes['id'] == 'workbench.parts.editor'
    except (KeyError, AttributeError):
        return False


def moveToCodepointOffset(
        self,
        codepointOffset: int,
):
    """
        This function moves textInfos by codepoint characters. A codepoint character represents exactly 1 character
        in a Pythonic string.

        Illustration:
            Suppose we have TextInfo that represents a paragraph of text:
            ```
            > s = paragraphInfo.text
            > s
            'Hello, world!\r'
            ```
            Suppose that we would like to put the cursor at the first letter of the word 'world'.
            That means jumping to index 7:
            ```
            > s[7:]
            'world!\r'
            ```
            Here is how this can be done:
            ```
            > info = paragraphInfo.moveToCodepointOffset(7)
            > info.setEndPoint(paragraphInfo, "endToEnd")
            > info.text
            'world!\r'
            ```

        Background:
            In many applications there is no one-to-one mapping of codepoint characters and TextInfo characters,
            e.g. when calling TextInfo.move(UNIT_CHARACTER, n).
            There are a couple of reasons for this discrepancy:
            1. In Wide character encoding, some 4-byte unicode characters are represented as two surrogate characters,
            whereas in Pythonic string they would be represented by a single character.
            2. In non-offset TextInfos (e.g. UIATextInfo)
            there is no guarantee on the fact that TextInfos.move(UNIT_CHARACTER, 1)would actually move by
            exactly 1 character.
            A good illustration of this is in Microsoft Word with UIA enabled always,
            the first character of a bullet list item would be represented by three pythonic codepoint characters:
            * Bullet character "•"
            * Tab character \t
            * And the first character of of list item per se.

            In many use cases (e.g., sentence navigation, style navigation),
            we identify pythonic codepoint character that we would like to move our TextInfo to.
            TextInfos.move(UNIT_CHARACTER, n) would cause many side effects.
            This function provides a clean and reliable way to jump to a given codepoint offset.

        Assumptions:
            1. This function operates on a non-collapsed TextInfo only. In a typical scenario, we might want
            to jump to a certain offset within a paragraph or a line. In this case this function
            should be called on TextInfo representing said paragraph or line.
            The reason for that is that for some implementations we might
            need to access text of paragraph/line in order to accurately compute result offset.
            2. It assumes that 1 character of application-specific TextInfo representation
            maps to 1 or more characters of codepoint representation.
            3. This function is also written with an assumption that a character
            in application-specific TextInfo representation might not map to any pythonic characters,
            although this scenario has never been observed in any applications.
            4. Also this function assumes that most characters have 1:1 mapping between codepoint
            and application-specific representations.
            This assumption is not required, however if this assumption is True, the function will converge faster.
            If this assumption is false, then it might take many iterations to find the right TextInfo.

        Algorithm:
            This generic implementation essentially a biased binary search.
            On every iteration we operate on a pythonic string and its TextInfo counterpart stored in info variable.
            We would like to reach a certain offset within that pythonic string,
            that is stored in codepointOffsetLeft variable.
            In every iteration of the loop:
            1. We try to either move from the left end of info by codepointOffsetLeft  characters
            or from the right end by -codepointOffsetRight characters - depending which move is shorter.
            We store destination point as collapsed TextInfo tmpInfo.
            2. We compute number of pythonic characters from the beginning of info until tmpInfo
            and store it in actualCodepointOffset variable.
            3. We will compare actualCodepointOffset with codepointOffsetLeft  : if they are equal,
            then we just found desired TextInfo.
            Otherwise we use tmpInfo as the middle point of binary search and we recurse either to the left
            or to the right, depending where desired offset lies.

            One extra part of the algorithm serves to prevent certain conditions:
            if we happen to move on the step 1 from the same point twice
            in two consecutive iterations of the loop, then on the second time we will move tmpInfo
            exactly to the opposite end of info,
            and the algorithm will fail on sanity check condition in the for loop.
            To avoid this situation we track last move and the direction of last divide
            in variables lastMove and lastRecursed.
            If we detect that we are about to move from the same endpoint for the second time,
            we reduce the count of characters in order to make sure
            the algorithm makes some progress on each iteration.
    """
    text = self.text
    if codepointOffset < 0 or codepointOffset > len(text):
        raise ValueError
    if codepointOffset == 0 or codepointOffset == len(text):
        result = self.copy()
        result.collapse(end=codepointOffset > 0)
        return result

    info = self.copy()
    # Total codepoint Length represents length in python characters of Current TextInfo we're workoing with.
    # We start with self, and then gradually divide and conquer in order to find desired offset.
    totalCodepointOffset = len(text)

    # codepointOffsetLeft and codepointOffsetRight represent distance in pythonic characters
    # from left and right ends of info correspondingly to the desired location.
    codepointOffsetLeft = codepointOffset
    codepointOffsetRight = totalCodepointOffset - codepointOffsetLeft

    # We store lastMove - by how many characters we moved last time, and
    # lastRecursed - whether last recursion happened to the left (-1), right(1) or failed due to overshooting(0)
    # in order to avoid certain corner cases.
    lastMove: int | None = None
    lastRecursed: int | None = None

    MAX_BINARY_SEARCH_ITERATIONS = 1000
    for __ in range(MAX_BINARY_SEARCH_ITERATIONS):
        tmpInfo = info.copy()
        if codepointOffsetLeft <= codepointOffsetRight:
            # Move from the left end of info. Let's compute by how many characters in moveCharacters variable.
            tmpInfo.collapse()
            if (
                lastRecursed is not None and (
                    lastRecursed == 0 or (
                        lastRecursed < 0 and lastMove > 0
                    )
                )
            ):
                # Here we check that last time we also attempted to move from the same left end.
                # And apparently we overshot last time. In order to avoid infinite loop
                # or overshooting again, reduce movement by half.
                moveCharacters = lastMove // 2
                if moveCharacters == 0 or moveCharacters >= lastMove:
                    raise RuntimeError("Unable to find desired offset in TextInfo.")
            else:
                moveCharacters = codepointOffsetLeft
            code = tmpInfo.move(UNIT_CHARACTER, moveCharacters, endPoint="end")
            lastMove = moveCharacters
            tmpText = tmpInfo.text
            actualCodepointOffset = len(tmpText)
            if not text.startswith(tmpText):
                raise RuntimeError(f"Inner textInfo text '{tmpText}' doesn't match outer textInfo text '{text}'")
            tmpInfo.collapse(end=True)
        else:
            # Move from the right end of info.
            tmpInfo.collapse(end=True)
            if (
                lastRecursed is not None and (
                    lastRecursed == 0 or (
                        lastRecursed > 0 and lastMove < 0
                    )
                )
            ):
                # lastMove was negative, inverting it since modular division of negative numbers works weird.
                moveCharacters = -((-lastMove) // 2)
                if moveCharacters == 0 or moveCharacters <= lastMove:
                    raise RuntimeError("Unable to find desired offset in TextInfo.")
            else:
                moveCharacters = -codepointOffsetRight
            code = tmpInfo.move(UNIT_CHARACTER, moveCharacters, endPoint="start")
            lastMove = moveCharacters
            tmpText = tmpInfo.text
            actualCodepointOffset = totalCodepointOffset - len(tmpText)
            if not text.endswith(tmpText):
                raise RuntimeError(f"Inner textInfo text '{tmpText}' doesn't match outer textInfo text '{text}'")
            tmpInfo.collapse()
        if code == 0:
            raise RuntimeError("Move by character operation unexpectedly failed.")
        if actualCodepointOffset <= 0 or actualCodepointOffset >= totalCodepointOffset:
            # We overshot, call this recursion attempt failed and try again lower movement
            lastRecursed = 0
            continue
        if actualCodepointOffset == codepointOffsetLeft:
            return tmpInfo
        elif actualCodepointOffset < codepointOffsetLeft:
            # Recursing right
            lastRecursed = 1
            text = text[actualCodepointOffset:]
            codepointOffsetLeft -= actualCodepointOffset
            totalCodepointOffset = codepointOffsetLeft + codepointOffsetRight
            info.setEndPoint(tmpInfo, which="startToStart")
        else:  # actualCodepointOffset > codepointOffsetLeft
            # Recursing left
            lastRecursed = -1
            text = text[:actualCodepointOffset]
            totalCodepointOffset = actualCodepointOffset
            codepointOffsetRight = totalCodepointOffset - codepointOffsetLeft
            info.setEndPoint(tmpInfo, which="endToEnd")
    raise RuntimeError("Infinite loop during binary search.")

class EditableIndentNav(NVDAObject):
    scriptCategory = _("IndentNav")
    beeper = Beeper()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vscodeTextProvider = None

    def getIndentLevel(self, s):
        if isBlank(s):
            return 0
        indent = speech.splitTextIndentation(s)[0]
        return len(indent.replace("\t", " " * 4))

    def isReportIndentWithTones(self):
        if BUILD_YEAR >= 2023:
            return config.conf["documentFormatting"]["reportLineIndentation"] >= ReportLineIndentation.TONES
        return config.conf["documentFormatting"]["reportLineIndentationWithTones"]

    def crackle(self, levels):
        if self.isReportIndentWithTones():
            self.beeper.fancyCrackle(levels, volume=getConfig("crackleVolume"))
        else:
            self.beeper.simpleCrackle(len(levels), volume=getConfig("crackleVolume"))


    @script(description=_("Moves to the next line with the same indentation level as the current line within the current indentation block."), gestures=['kb:NVDA+alt+DownArrow'])
    def script_moveToNextSibling(self, gesture):
        # Translators: error message if next sibling couldn't be found (in editable control or in browser)
        msgEditable = _("No next line within indentation block")
        self.move(1, [msgEditable])


    @script(description=_("Moves to the next line with the same indentation level as the current line within the current indentation block and skipping over clutter."), gestures=['kb:NVDA+alt+windows+DownArrow'])
    def script_moveToNextSiblingSkipClutter(self, gesture):
        # Translators: error message if next sibling couldn't be found (in editable control or in browser)
        msgEditable = _("No next line within indentation block")
        self.move(1, [msgEditable], excludeFilterRegex=re.compile(getConfig("clutterRegex")))

    @script(description=_("Moves to the next line with the same indentation level as the current line potentially in the following indentation block."), gestures=['kb:NVDA+alt+control+DownArrow'])
    def script_moveToNextSiblingForce(self, gesture):
        # Translators: error message if next sibling couldn't be found in editable control (forced command)
        msgEditable = _("No next line in the document")
        self.move(1, [msgEditable], unbounded=True)


    @script(description=_("Moves to the last line with the same indentation level as the current line within the current indentation block."), gestures=['kb:NVDA+alt+shift+DownArrow'])
    def script_moveToLastSibling(self, gesture):
        # Translators: error message if last sibling couldn't be found in editable control (forced command)
        msgEditable = _("No next line in the document")
        self.move(1, [msgEditable], moveCount=1000)

    @script(description=_("Moves to the previous line with the same indentation level as the current line within the current indentation block."), gestures=['kb:NVDA+alt+UpArrow'])
    def script_moveToPreviousSibling(self, gesture):
        # Translators: error message if previous sibling couldn't be found (in editable control or in browser)
        msgEditable = _("No previous line within indentation block")
        self.move(-1, [msgEditable])

    @script(description=_("Moves to the previous line with the same indentation level as the current line within the current indentation block and skipping over clutter."), gestures=['kb:NVDA+windows+alt+UpArrow'])
    def script_moveToPreviousSiblingSkipClutter(self, gesture):
        # Translators: error message if previous sibling couldn't be found (in editable control or in browser)
        msgEditable = _("No previous line within indentation block")
        self.move(-1, [msgEditable], excludeFilterRegex=re.compile(getConfig("clutterRegex")))


    @script(description=_("Moves to the previous line with the same indentation level as the current line potentially in the preceding indentation block."), gestures=['kb:NVDA+alt+control+UpArrow'])
    def script_moveToPreviousSiblingForce(self, gesture):
        # Translators: error message if previous sibling couldn't be found in editable control (forced command)
        msgEditable = _("No previous line in the document")
        self.move(-1, [msgEditable], unbounded=True)

    @script(description=_("Moves to the first line with the same indentation level as the current line within the current indentation block."), gestures=['kb:NVDA+alt+shift+UpArrow'])
    def script_moveToFirstSibling(self, gesture):
        # Translators: error message if first sibling couldn't be found in editable control (forced command)
        msgEditable = _("No previous line in the document")
        self.move(-1, [msgEditable], moveCount=1000)

    @script(description=_("Speak parent line."), gestures=['kb:NVDA+I'])
    def script_speakParent(self, gesture):
        focus = api.getFocusObject()
        count=scriptHandler.getLastScriptRepeatCount()
        # Translators: error message if parent couldn't be found (in editable control or in browser)
        msgEditable = _("No parent of indentation block")
        self.move(-1, [msgEditable], unbounded=True, op=operator.lt, speakOnly=True, moveCount=count+1)

    def move(self, increment, errorMessages, unbounded=False, op=operator.eq, speakOnly=False, moveCount=1, excludeFilterRegex=None):
        """Moves to another line in current document.
        This function will call one of its implementations dependingon whether the focus is in an editable text or in a browser.
        @paramincrement: Direction to move, should be either 1 or -1.
        @param errorMessages: Error message to speak if the desired line cannot be found.
        @param unbounded: When in an indented text file whether to allow to jump to another indentation block.
        For example, in a python source code, when set to True, it will be able to jump from the body of one function to another.
        When set to false, it will be constrained within the current indentation block, suchas a function.
        @param op: Operator that is applied to the indentation level of lines being searched.
        This operator should returntrue only on the desired string.
        For example, when looking for a string of the same indent, this should be operator.eq.
        When searching for a string with greater indent, this should be set to operator.gt, and so on.
        @param speakOnly: only speak the line, don't move the cursor there
        @param moveCount: perform move operation this many times.
        """
        focus = api.getFocusObject()
        self.moveInEditable(increment, errorMessages[0], unbounded, op, speakOnly=speakOnly, moveCount=moveCount, excludeFilterRegex=excludeFilterRegex)

    def moveInEditable(self, increment, errorMessage, unbounded=False, op=operator.eq, speakOnly=False, moveCount=1, excludeFilterRegex=None):
        try:
            with self.getLineManager() as lm:
                self.addHistory(lm.lineIndex)
                # Get the current indentation level
                text = lm.getText()
                indentationLevel = self.getIndentLevel(text)
                onEmptyLine = isBlank(text)

                # Scan each line until we hit the end of the indentation block, the end of the edit area, or find a line with the same indentation level
                found = False
                indentLevels = []
                while True:
                    result = lm.move(increment)
                    if result == 0:
                        break
                    text = lm.getText()
                    newIndentation = self.getIndentLevel(text)

                    # Skip over empty lines if we didn't start on one.
                    if not onEmptyLine and isBlank(text):
                        continue

                    if op(newIndentation, indentationLevel):
                        if excludeFilterRegex is  None or not excludeFilterRegex.match(text):
                            # Found it
                            found = True
                            indentationLevel = newIndentation
                            resultLine = lm.getLine()
                            resultText = lm.getText()
                            moveCount -= 1
                            if moveCount == 0:
                                break
                    elif newIndentation < indentationLevel:
                        # Not found in this indentation block
                        if not unbounded:
                            break
                    indentLevels.append(newIndentation )
                if found:
                    textInfo = None
                    if not speakOnly:
                        textInfo = lm.updateCaret(resultLine)
                        self.addHistory(resultLine)
                    self.crackle(indentLevels)
                    if textInfo is not None:
                        speech.speakTextInfo(textInfo, unit=textInfos.UNIT_LINE)
                    else:
                        speech.speakText(resultText)
                else:
                    self.endOfDocument(errorMessage)
        except TextInfoUnavailableException:
            VSCodeRequestDialog(gui.mainFrame, self.appModule).Show()
        except VSCodeNotMainEditorException:
            msg = _("Cannot use IndentNav not in the main editor of VSCode")
            self.endOfDocument(msg)

    def getLineManager(self, selectionMode=False):
        return FastLineManagerV2(self, selectionMode)

    @script(description=_("Moves to the next line with a greater indentation level than the current line within the current indentation block."), gestures=['kb:NVDA+alt+RightArrow'])
    def script_moveToChild(self, gesture):
        # Translators: error message if a child couldn't be found (in editable control or in browser)
        msgEditable = _("No child block within indentation block")
        self.move(1, [msgEditable], unbounded=False, op=operator.gt)

    @script(description=_("Moves to the previous line with a lesser indentation level than the current line within the current indentation block."), gestures=['kb:NVDA+alt+LeftArrow'])
    def script_moveToParent(self, gesture):
        # Translators: error message if parent couldn't be found (in editable control or in browser)
        msgEditable = _("No parent of indentation block")
        self.move(-1, [msgEditable], unbounded=True, op=operator.lt)

    @script(description=_("Moves to the previous line with a greater indentation level than the current line within the current indentation block."), gestures=['kb:NVDA+control+alt+RightArrow'])
    def script_moveToPreviousChild(self, gesture):
        # Translators: error message if a previous child couldn't be found (in editable control)
        msgEditable = _("No previous child block within indentation block")
        self.move(-1, [msgEditable], unbounded=False, op=operator.gt)

    @script(description=_("Moves to the next line with a lesser indentation level than the current line within the current indentation block."), gestures=['kb:NVDA+control+alt+LeftArrow'])
    def script_moveToNextParent(self, gesture):
        # Translators: error message if previous parent couldn't be found (in editable control)
        msgEditable = _("No next parent of indentation block")
        self.move(1, [msgEditable], unbounded=True, op=operator.lt)

    @script(description=_("Select current indentation block. Press twice to copy to clipboard."), gestures=['kb:NVDA+control+i'])
    def script_selectSingleIndentationBlock(self, gesture):
        msg = _("Indent block copied to clipboard. ")
        self.selectIndentationBlock(selectMultiple=False, successMessage=msg)

    @script(description=_("Select current indentation block, as well as follwoing blocks of the same level. Press twice to copy to clipboard."), gestures=['kb:NVDA+alt+i'])
    def script_selectMultipleIndentationBlocks(self, gesture):
        msg = _("Indent blocks copied to clipboard. ")
        self.selectIndentationBlock(selectMultiple=True, successMessage=msg)

    def selectIndentationBlock(self, selectMultiple=False, successMessage=""):
        count=scriptHandler.getLastScriptRepeatCount()
        if selectMultiple and count >= 1:
            # Just copy selection to the clipboard
            focus = api.getFocusObject()
            textInfo = focus.makeTextInfo(textInfos.POSITION_SELECTION)
            api.copyToClip(textInfo.text)
            ui.message(successMessage)
        with self.getLineManager(selectionMode=True) as lm:
            # Get the current indentation level
            text = lm.getText()
            originalTextInfo = lm.getTextInfo()
            indentationLevel = self.getIndentLevel(text)
            onEmptyLine = isBlank(text)
            if onEmptyLine:
                return self.endOfDocument(_("Nothing to select"))
            # Scan each line forward as long as indentation level is greater than current
            line = lm.getLine()
            indentLevels = []
            while True:
                result = lm.move(1)
                if result == 0:
                    if not selectMultiple and count >= 1:
                        core.callLater(100, self.endOfDocument, _("No more indentation blocks!"))
                    break
                text = lm.getText()
                newIndentation = self.getIndentLevel(text)

                if  isBlank(text):
                    continue

                if newIndentation < indentationLevel:
                    if not selectMultiple and count >= 1:
                        core.callLater(100, self.endOfDocument, _("No more indentation blocks!"))
                        #self.endOfDocument(_("No more indentation blocks!"))
                    break
                elif newIndentation == indentationLevel:
                    if   selectMultiple:
                        pass
                    elif count > 0:
                        count -= 1
                    else:
                        break
                else: # newIndentation > indentationLevel
                    pass
                line = lm.getLine()
                indentLevels.append(newIndentation )
            selection = originalTextInfo.copy()
            if line is not None:
                textInfo = lm.getTextInfo(line)
                selection.setEndPoint(textInfo, "endToEnd")
            selection.updateSelection()
            self.crackle(indentLevels)
            speech.speakTextInfo(textInfo, unit=textInfos.UNIT_LINE)

    @script(description=_("Indent-paste. This will figure out indentation level in the current line and paste text from clipboard adjusting indentation level correspondingly."), gestures=['kb:NVDA+V'])
    def script_indentPaste(self, gesture):
        clipboardBackup = api.getClipData()
        try:
            focus = api.getFocusObject()
            selection = focus.makeTextInfo(textInfos.POSITION_SELECTION)
            if len(selection.text) != 0:
                ui.message(_("Some text selected! Cannot indent-paste."))
                return
            line = focus.makeTextInfo(textInfos.POSITION_CARET)
            line.collapse()
            line.expand(textInfos.UNIT_LINE)
            # Make sure line doesn't include newline characters
            while len(line.text) > 0 and line.text[-1] in "\r\n":
                if 0 == line.move(textInfos.UNIT_CHARACTER, -1, "end"):
                    break
            lineLevel = self.getIndentLevel(line.text.rstrip("\r\n") + "a")
            if not isBlank(line.text):
                ui.message(_("Cannot indent-paste: current line is not empty!"))
                return
            text = clipboardBackup
            textLevel = min([
                self.getIndentLevel(s)
                for s in text.splitlines()
                if not isBlank(s)
            ])
            useTabs = '\t' in text or '\t' in line.text
            delta = lineLevel - textLevel
            text = text.replace("\t", " "*4)
            if delta > 0:
                text = "\n".join([
                    " "*delta + s
                    for s in text.splitlines()
                ])
            elif delta < 0:
                text = "\n".join([
                    s[min(-delta, len(s)):]
                    for s in text.splitlines()
                ])
            if useTabs:
                text = text.replace(" "*4, "\t")
            api.copyToClip(text)
            line.updateSelection()
            time.sleep(0.1)
            keyboardHandler.KeyboardInputGesture.fromName("Control+v").send()
            core.callLater(100, ui.message, _("Pasted"))
        finally:
            core.callLater(100, api.copyToClip, clipboardBackup)

    def getHistory(self):
        try:
            return self.linesHistory, self.historyIndex
        except AttributeError:
            self.linesHistory = []
            self.historyIndex = -1
            return self.linesHistory, self.historyIndex

    def addHistory(self, lineNumber):
        history, index = self.getHistory()
        try:
            if history[index] == lineNumber:
                return
        except IndexError:
            pass
        self.historyIndex += 1
        self.linesHistory.insert(self.historyIndex, lineNumber)
        if len(self.linesHistory) > self.historyIndex + 1:
            self.linesHistory = self.linesHistory[:self.historyIndex + 1]


    @script(description=_("Go back in history."), gestures=['kb:NVDA+control+u'])
    def script_goBack(self, gesture):
        lines, index = self.getHistory()
        if index > 0:
            with self.getLineManager() as lm:
                currentLineIndex = lm.lineIndex
                if currentLineIndex == lines[index]:
                    index -= 1
                self.historyIndex = index
                lineNumber = lines[index]
                textInfo = lm.updateCaret(lineNumber)
                speech.speakTextInfo(textInfo, unit=textInfos.UNIT_LINE)
        else:
            self.endOfDocument(_(")No previous line in history"))

    @script(description=_("Go forward in history."), gestures=['kb:NVDA+alt+u'])
    def script_goForward(self, gesture):
        lines, index = self.getHistory()
        index += 1
        try:
            lineNumber = lines[index]
        except IndexError:
            self.endOfDocument(_(")No next line in history"))
            return
        self.historyIndex = index
        with self.getLineManager() as lm:
                textInfo = lm.updateCaret(lineNumber)
                speech.speakTextInfo(textInfo, unit=textInfos.UNIT_LINE)

    def endOfDocument(self, message=None):
        volume = getConfig("noNextTextChimeVolume")
        self.beeper.fancyBeep("HF", 100, volume, volume)
        if getConfig("noNextTextMessage") and message is not None:
            ui.message(message)

    def isVscodeApp(self):
        try:
            if self.treeInterceptor is not None:
                return False
        except NameError:
            return False
        productName = self.appModule.productName or ""
        return productName.startswith("Visual Studio Code")

    def getPiper(self):
        try:
            if self.piper is not None:
                return self.piper
        except AttributeError:
            pass
        focus = api.getFocusObject()
        if self != focus:
            raise RuntimeError("Can only create VSCode piper for focused object")
        piper = getPiperForFocus()
        if piper is not None:
            self.piper = piper
            return piper
        return None



    def makeEnhancedTextInfo(
        self,
        position,
        allowPlainTextInfoInVSCode=False,
    ):
        if not self.isVscodeApp():
            return self.makeTextInfo(position)
        if not isVSCodeMainEditor(self):
            raise VSCodeNotMainEditorException()
        piper = self.getPiper()
        if piper is not None:
            return VSCodeTextInfo(self, position)
        if allowPlainTextInfoInVSCode:
            return self.makeTextInfo(position)
        return None

    @script(description=_("IndentNav QuickFind generic script"), gestures=['kb:Windows+z'])
    def script_quickFind(self, gesture):
        if not isinstance(gesture, keyboardHandler.KeyboardInputGesture):
            log.warning(f"Got unexpected gesture type: {gesture}")
            return
        keystroke =         getKeystrokeFromGesture(gesture)
        SHIFT_MODIFIER = "shift+"
        shift = SHIFT_MODIFIER in keystroke
        keystroke = keystroke.replace(SHIFT_MODIFIER, '')
        global globalBookmarks
        try:
            bookmark = globalBookmarks[keystroke]
        except KeyError:
            log.warning(f"Unable to find bookmark for keystroke {keystroke}")
            return
        self.doQuickFind(bookmark, -1 if shift else 1)

    def doQuickFind(self, bookmark, direction):
        caretInfo = self.makeEnhancedTextInfo(textInfos.POSITION_SELECTION)
        caretInfo.collapse(end=(direction > 0))
        info = self.makeEnhancedTextInfo(textInfos.POSITION_ALL)
        info.setEndPoint(caretInfo, 'startToStart' if direction > 0 else 'endToEnd')
        text = info.text
        text = re.sub(r'\r(?!\n)', '\n', text)
        matches = list(re.finditer(bookmark.pattern, text, re.MULTILINE))
        if len(matches) == 0:
            self.endOfDocument(_("Bookmark not found"))
            return
        match = matches[0 if direction > 0 else -1]
        startIndex = match.start()
        endIndex = match.end()
        compoundMode = False
        if isinstance(info, CompoundTextInfo):
            if info._start == info._end and  isinstance(info._start, OffsetsTextInfo):
                compoundMode = True
                outerTextInfo = info
                info = outerTextInfo._start
        if isinstance(info, OffsetsTextInfo):
            converter = textUtils.getOffsetConverter(info.encoding)(text)
            startOffset, endOffset = converter.strToEncodedOffsets(startIndex, endIndex)
            selectionInfo = info.copy()
            selectionInfo.collapse()
            selectionInfo._startOffset += startOffset
            selectionInfo._endOffset += endOffset
        else:
            startInfo = moveToCodepointOffset(info, startIndex)
            endInfo = moveToCodepointOffset(info, endIndex)
            selectionInfo = startInfo.copy()
            selectionInfo.setEndPoint(endInfo, 'endToEnd')
        if compoundMode:
            outerTextInfo = outerTextInfo.copy()
            outerTextInfo._start = outerTextInfo._end = selectionInfo
            selectionInfo = outerTextInfo
        selectionInfo.updateSelection()
        lineInfo = selectionInfo.copy()
        unit = textInfos.UNIT_LINE if isinstance(lineInfo, VsWpfTextViewTextInfo) else textInfos.UNIT_PARAGRAPH
        lineInfo.expand(unit)
        lineInfo.setEndPoint(selectionInfo, 'startToStart')
        speech.speakTextInfo(lineInfo, unit=unit, reason=controlTypes.OutputReason.CARET)

    @script(description=_("Speak current line"), gestures=['kb:NVDA+Control+l'])
    def script_speakCurrentLine(self, gesture):
        return globalCommands.commands.script_review_currentLine(gesture)
        
    #@script(description=_("Debug"), gestures=['kb:control+shift+nvda'])
    def script_debug(self, gesture):
        with self.getLineManager() as lm:
            api.lm = lm
            tones.beep(500, 50)
