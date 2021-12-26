#A part of the IndentNav addon for NVDA
#Copyright (C) 2017-2021 Tony Malykh
#This file is covered by the GNU General Public License.
#See the file LICENSE  for more details.

# This addon allows to navigate documents by indentation or offset level.
# In browsers you can navigate by object location on the screen.
# In editable text fields you can navigate by the indentation level.
# This is useful for editing source code.
# Author: Tony Malykh <anton.malykh@gmail.com>
# https://github.com/mltony/nvda-indent-nav/
# Original author: Sean Mealin <spmealin@gmail.com>

import addonHandler
import api
import controlTypes
import config
import core
import ctypes
from enum import Enum, auto
import globalPluginHandler
import gui
from gui.settingsDialogs import SettingsPanel
import keyboardHandler
import NVDAHelper
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.IAccessible import IA2TextTextInfo
from NVDAObjects.IAccessible.ia2TextMozilla import MozillaCompoundTextInfo
from NVDAObjects import NVDAObject
import operator
import re
import scriptHandler
from scriptHandler import script
import speech
import struct
import textInfos
import time
import tones
import ui
import wx

try:
    ROLE_EDITABLETEXT = controlTypes.ROLE_EDITABLETEXT
    ROLE_TREEVIEWITEM = controlTypes.ROLE_TREEVIEWITEM
except AttributeError:
    ROLE_EDITABLETEXT = controlTypes.Role.EDITABLETEXT
    ROLE_TREEVIEWITEM = controlTypes.Role.TREEVIEWITEM

debug = False
if debug:
    import threading
    LOG_FILE_NAME = "C:\\Users\\tony\\Dropbox\\3.txt"
    f = open(LOG_FILE_NAME, "w", encoding='utf=8')
    f.close()
    LOG_MUTEX = threading.Lock()
    def mylog(s):
        with LOG_MUTEX:
            f = open(LOG_FILE_NAME, "a", encoding='utf-8')
            print(s, file=f)
            #f.write(s.encode('UTF-8'))
            #f.write('\n')
            f.close()
else:
    def mylog(*arg, **kwarg):
        pass



def myAssert(condition):
    if not condition:
        raise RuntimeError("Assertion failed")

def initConfiguration():
    confspec = {
        "crackleVolume" : "integer( default=25, min=0, max=100)",
        "noNextTextChimeVolume" : "integer( default=50, min=0, max=100)",
        "noNextTextMessage" : "boolean( default=False)",
    }
    config.conf.spec["indentnav"] = confspec

def getConfig(key):
    value = config.conf["indentnav"][key]
    return value

def setConfig(key, value):
    config.conf["indentnav"][key] = value


addonHandler.initTranslation()
initConfiguration()


class SettingsDialog(SettingsPanel):
    # Translators: Title for the settings dialog
    title = _("IndentNav settings")

    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

    def makeSettings(self, settingsSizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
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

      # Checkboxes
        # Translators: Checkbox that controls spoken message when no next or previous text paragraph is available in the document
        label = _("Speak message when no next paragraph containing text available in the document")
        self.noNextTextMessageCheckbox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.noNextTextMessageCheckbox.Value = getConfig("noNextTextMessage")


    def onSave(self):
        config.conf["indentnav"]["crackleVolume"] = self.crackleVolumeSlider.Value
        config.conf["indentnav"]["noNextTextChimeVolume"] = self.noNextTextChimeVolumeSlider.Value
        config.conf["indentnav"]["noNextTextMessage"] = self.noNextTextMessageCheckbox.Value

# Browse mode constants:
BROWSE_MODES = [
    _("horizontal offset"),
    _("font size"),
    _("font size and same style"),
]

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("IndentNav")
    def __init__(self, *args, **kwargs):
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        self.createMenu()

    def terminate(self):
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SettingsDialog)

    def createMenu(self):
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SettingsDialog)

    def chooseNVDAObjectOverlayClasses (self, obj, clsList):
        if obj.windowClassName == u'Scintilla':
            clsList.append(EditableIndentNav)
            return
        if obj.windowClassName == u"AkelEditW":
            clsList.append(EditableIndentNav)
            return
        if obj.role == ROLE_EDITABLETEXT:
            clsList.append(EditableIndentNav)
            return
        if obj.role == ROLE_TREEVIEWITEM:
            clsList.append(TreeIndentNav)
            return

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


class TraditionalLineManager:
    """
    This class is no longer used - please use FastLineManager instead.
    """
    def __init__(self):
        pass

    def __enter__(self):
        focus = api.getFocusObject()
        self.textInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def move(self, increment):
        result = self.textInfo.move(textInfos.UNIT_LINE, increment)
        return result

    def getText(self):
        self.textInfo.expand(textInfos.UNIT_LINE)
        return self.textInfo.text

    def getLine(self):
        return self.textInfo.copy()

    def updateCaret(self, line):
        line.updateCaret()
class OffsetMode(Enum):
    GENERIC = auto()
    OFFSET = auto()
    COMPOUND = auto()

class OffsetDecodeMode(Enum):
    NONE = auto()
    PLAIN = auto()
    UTF8 = auto()

class FastLineManager:
    def __init__(self):
        pass

    def __enter__(self):
        focus = api.getFocusObject()
        document = focus.makeTextInfo(textInfos.POSITION_ALL)
        pretext = focus.makeTextInfo(textInfos.POSITION_SELECTION)
        pretext.collapse()
        pretext.setEndPoint(document, "startToStart")
        self.lineIndex = len(self.normalizeString(pretext.text).split("\n")) - 1
        self.originalLineIndex = self.lineIndex
        documentText = document.text
        text = self.normalizeString(documentText)
        self.lines = text.split("\n")
        self.nLines = len(self.lines)
        self.originalCaret = focus.makeTextInfo(textInfos.POSITION_SELECTION)
        self.originalCaret.collapse()
        self.originalCaret.expand(textInfos.UNIT_LINE)
        self.numNewLineCharacters = 2 if "\r\n" in document.text else 1
        self.offsetMode = OffsetMode.GENERIC
        if isinstance(document, textInfos.offsets.OffsetsTextInfo):
            self.offsetMode = OffsetMode.OFFSET
            # In some apps, like notepad, end offset is computed incorrectly. The last characters appear to be empty.
            #Working around this here
            lastChar = document.copy()
            while lastChar._endOffset >= 1:
                lastChar._startOffset = lastChar._endOffset - 1
                if len(lastChar.text) == 0:
                    lastChar._endOffset -= 1
                else:
                    break
            endOffset = lastChar._endOffset
        if isinstance(document, MozillaCompoundTextInfo):
            if isinstance(document._start, IA2TextTextInfo) and isinstance(document._end, IA2TextTextInfo):
                if document._start._obj == document._end._obj:
                    self.offsetMode = OffsetMode.COMPOUND
                    endOffset = document._end._endOffset
        if self.offsetMode in {OffsetMode.OFFSET, OffsetMode.COMPOUND}:
            if len(document.text) == endOffset:
                self.decoding = OffsetDecodeMode.PLAIN
            elif len(document.text.encode('utf-8')) == endOffset:
                self.decoding = OffsetDecodeMode.UTF8
            else:
                # We don't know how to decode text into offsets. Fall back to more reliable version.
                self.offsetMode = OffsetMode.GENERIC
                self.decoding = OffsetDecodeMode.NONE
            def speakMode():
                speech.cancelSpeech()
                ui.message(f"{self.offsetMode} {self.decoding}")
            #core.callLater(1000, speakMode)
        self.document = document
        #self.offsetMode = OffsetMode.GENERIC
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

    def getTextInfo(self, line=None):
        if line is None:
            line = self.lineIndex
        if self.offsetMode in {OffsetMode.OFFSET, OffsetMode.COMPOUND}:
            textInfo = self.document.copy()
            decoding = self.decoding
            numNewLineCharacters = self.numNewLineCharacters
            def l(s):
                if decoding == OffsetDecodeMode.UTF8:
                    s = s.encode('utf-8')
                return numNewLineCharacters + len(s)
            startOffset = sum([ l(s) for s in self.lines[:line]])
            endOffset = startOffset + l(self.lines[line])
            if self.offsetMode == OffsetMode.OFFSET:
                textInfo._startOffset = startOffset
                textInfo._endOffset = min(textInfo._endOffset, endOffset)
            elif self.offsetMode == OffsetMode.COMPOUND:
                textInfo._start._startOffset = startOffset
                textInfo._end._startOffset = startOffset
                textInfo._start._endOffset = min(textInfo._start._endOffset, endOffset)
                textInfo._end._endOffset = min(textInfo._end._endOffset, endOffset)
            else:
                raise Exception("impossible")
            return textInfo
            
        delta = line - self.originalLineIndex
        textInfo = self.originalCaret.copy()
        result = textInfo.move(textInfos.UNIT_LINE, delta)
        if result != delta:
            raise Exception(f"Failed to move by {delta} lines")
        textInfo.expand(textInfos.UNIT_LINE)
        return textInfo

    def normalizeString(self, s):
        s = s.replace("\r\n", "\n")
        s = s.replace("\r", "\n")
        return s

class EditableIndentNav(NVDAObject):
    scriptCategory = _("IndentNav")
    beeper = Beeper()
    def getIndentLevel(self, s):
        if speech.isBlank(s):
            return 0
        indent = speech.splitTextIndentation(s)[0]
        return len(indent.replace("\t", " " * 4))

    def isReportIndentWithTones(self):
        return config.conf["documentFormatting"]["reportLineIndentationWithTones"]

    def crackle(self, levels):
        if self.isReportIndentWithTones():
            self.beeper.fancyCrackle(levels, volume=getConfig("crackleVolume"))
        else:
            self.beeper.simpleCrackle(len(levels), volume=getConfig("crackleVolume"))


    @script(description="Moves to the next line with the same indentation level as the current line within the current indentation block.", gestures=['kb:NVDA+alt+DownArrow'])
    def script_moveToNextSibling(self, gesture):
        # Translators: error message if next sibling couldn't be found (in editable control or in browser)
        msgEditable = _("No next line within indentation block")
        self.move(1, [msgEditable])

    @script(description="Moves to the next line with the same indentation level as the current line potentially in the following indentation block.", gestures=['kb:NVDA+alt+control+DownArrow'])
    def script_moveToNextSiblingForce(self, gesture):
        # Translators: error message if next sibling couldn't be found in editable control (forced command)
        msgEditable = _("No next line in the document")
        self.move(1, [msgEditable], unbounded=True)


    @script(description="Moves to the last line with the same indentation level as the current line within the current indentation block.", gestures=['kb:NVDA+alt+shift+DownArrow'])
    def script_moveToLastSibling(self, gesture):
        # Translators: error message if last sibling couldn't be found in editable control (forced command)
        msgEditable = _("No next line in the document")
        self.move(1, [msgEditable], moveCount=1000)

    @script(description="Moves to the previous line with the same indentation level as the current line within the current indentation block.", gestures=['kb:NVDA+alt+UpArrow'])
    def script_moveToPreviousSibling(self, gesture):
        # Translators: error message if previous sibling couldn't be found (in editable control or in browser)
        msgEditable = _("No previous line within indentation block")
        self.move(-1, [msgEditable])

    @script(description="Moves to the previous line with the same indentation level as the current line within the current indentation block.", gestures=['kb:NVDA+alt+control+UpArrow'])
    def script_moveToPreviousSiblingForce(self, gesture):
        # Translators: error message if previous sibling couldn't be found in editable control (forced command)
        msgEditable = _("No previous line in the document")
        self.move(-1, [msgEditable], unbounded=True)

    @script(description="Moves to the first line with the same indentation level as the current line within the current indentation block.", gestures=['kb:NVDA+alt+shift+UpArrow'])
    def script_moveToFirstSibling(self, gesture):
        # Translators: error message if first sibling couldn't be found in editable control (forced command)
        msgEditable = _("No previous line in the document")
        self.move(-1, [msgEditable], moveCount=1000)

    @script(description="Speak parent line.", gestures=['kb:NVDA+I'])
    def script_speakParent(self, gesture):
        focus = api.getFocusObject()
        count=scriptHandler.getLastScriptRepeatCount()
        # Translators: error message if parent couldn't be found (in editable control or in browser)
        msgEditable = _("No parent of indentation block")
        self.move(-1, [msgEditable], unbounded=True, op=operator.lt, speakOnly=True, moveCount=count+1)

    def move(self, increment, errorMessages, unbounded=False, op=operator.eq, speakOnly=False, moveCount=1,):
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
        self.moveInEditable(increment, errorMessages[0], unbounded, op, speakOnly=speakOnly, moveCount=moveCount)

    def moveInEditable(self, increment, errorMessage, unbounded=False, op=operator.eq, speakOnly=False, moveCount=1):
        with self.getLineManager() as lm:
            # Get the current indentation level
            text = lm.getText()
            indentationLevel = self.getIndentLevel(text)
            onEmptyLine = speech.isBlank(text)

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
                if not onEmptyLine and speech.isBlank(text):
                    continue

                if op(newIndentation, indentationLevel):
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
                self.crackle(indentLevels)
                if textInfo is not None:
                    speech.speakTextInfo(textInfo, unit=textInfos.UNIT_LINE)
                else:
                    speech.speakText(resultText)
            else:
                self.endOfDocument(errorMessage)

    def getLineManager(self):
        return FastLineManager()

    @script(description="Moves to the next line with a greater indentation level than the current line within the current indentation block.", gestures=['kb:NVDA+alt+RightArrow'])
    def script_moveToChild(self, gesture):
        # Translators: error message if a child couldn't be found (in editable control or in browser)
        msgEditable = _("No child block within indentation block")
        self.move(1, [msgEditable], unbounded=False, op=operator.gt)

    @script(description="Moves to the previous line with a lesser indentation level than the current line within the current indentation block.", gestures=['kb:NVDA+alt+LeftArrow'])
    def script_moveToParent(self, gesture):
        # Translators: error message if parent couldn't be found (in editable control or in browser)
        msgEditable = _("No parent of indentation block")
        self.move(-1, [msgEditable], unbounded=True, op=operator.lt)

    @script(description="Moves to the previous line with a greater indentation level than the current line within the current indentation block.", gestures=['kb:NVDA+control+alt+RightArrow'])
    def script_moveToPreviousChild(self, gesture):
        # Translators: error message if a previous child couldn't be found (in editable control)
        msgEditable = _("No previous child block within indentation block")
        self.move(-1, [msgEditable], unbounded=False, op=operator.gt)

    @script(description="Moves to the next line with a lesser indentation level than the current line within the current indentation block.", gestures=['kb:NVDA+control+alt+LeftArrow'])
    def script_moveToNextParent(self, gesture):
        # Translators: error message if previous parent couldn't be found (in editable control)
        msgEditable = _("No next parent of indentation block")
        self.move(1, [msgEditable], unbounded=True, op=operator.lt)

    @script(description="Select current indentation block. Press twice to copy to clipboard.", gestures=['kb:NVDA+control+i'])
    def script_selectSingleIndentationBlock(self, gesture):
        msg = _("Indent block copied to clipboard. ")
        self.selectIndentationBlock(selectMultiple=False, successMessage=msg)

    @script(description="Select current indentation block, as well as follwoing blocks of the same level. Press twice to copy to clipboard.", gestures=['kb:NVDA+alt+i'])
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
        with self.getLineManager() as lm:
            if count >= 1:
                textInfo = lm.getTextInfo()
                textInfo.collapse()
                textInfo.updateCaret()
            # Get the current indentation level
            text = lm.getText()
            originalTextInfo = lm.getTextInfo()
            indentationLevel = self.getIndentLevel(text)
            onEmptyLine = speech.isBlank(text)
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

                if  speech.isBlank(text):
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
            
    @script(description="Indent-paste. This will figure out indentation level in the current line and paste text from clipboard adjusting indentation level correspondingly.", gestures=['kb:NVDA+V'])
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
            if not speech.isBlank(line.text):
                ui.message(_("Cannot indent-paste: current line is not empty!"))
                return
            text = clipboardBackup
            textLevel = min([
                self.getIndentLevel(s)
                for s in text.splitlines()
                if not speech.isBlank(s)
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
            

    def endOfDocument(self, message):
        volume = getConfig("noNextTextChimeVolume")
        self.beeper.fancyBeep("HF", 100, volume, volume)
        if getConfig("noNextTextMessage"):
            ui.message(message)

class TreeIndentNav(NVDAObject):
    scriptCategory = _("IndentNav")
    beeper = Beeper()

    @script(description="Moves to the next item on the same level within current subtree.", gestures=['kb:NVDA+alt+DownArrow'])
    def script_moveToNextSibling(self, gesture):
        # Translators: error message if next sibling couldn't be found in Tree view
        errorMsg = _("No next item on the same level within this subtree")
        self.moveInTree(1, errorMsg, op=operator.eq)

    @script(description="Moves to the previous item on the same level within current subtree.", gestures=['kb:NVDA+alt+UpArrow'])
    def script_moveToPreviousSibling(self, gesture):
        # Translators: error message if next sibling couldn't be found in Tree view
        errorMsg = _("No previous item on the same level within this subtree")
        self.moveInTree(-1, errorMsg, op=operator.eq)

    @script(description="Moves to the next item on the same level.", gestures=['kb:NVDA+Control+alt+DownArrow'])
    def script_moveToNextSiblingForce(self, gesture):
        # Translators: error message if next sibling couldn't be found in Tree view
        errorMsg = _("No next item on the same level in this tree view")
        self.moveInTree(1, errorMsg, op=operator.eq, unbounded=True)

    @script(description="Moves to the previous item on the same level.", gestures=['kb:NVDA+Control+alt+UpArrow'])
    def script_moveToPreviousSiblingForce(self, gesture):
        # Translators: error message if previous sibling couldn't be found in Tree view
        errorMsg = _("No previous item on the same level in this tree view")
        self.moveInTree(-1, errorMsg, op=operator.eq, unbounded=True)

    @script(description="Moves to the last item on the same level within current subtree.", gestures=['kb:NVDA+alt+Shift+DownArrow'])
    def script_moveToLastSibling(self, gesture):
        # Translators: error message if next sibling couldn't be found in Tree view
        errorMsg = _("No next item on the same level within this subtree")
        self.moveInTree(1, errorMsg, op=operator.eq, moveCount=1000)

    @script(description="Moves to the first item on the same level within current subtree.", gestures=['kb:NVDA+alt+Shift+UpArrow'])
    def script_moveToFirstSibling(self, gesture):
        # Translators: error message if next sibling couldn't be found in Tree view
        errorMsg = _("No previous item on the same level within this subtree")
        self.moveInTree(-1, errorMsg, op=operator.eq, moveCount=1000)

    @script(description="Speak parent item.", gestures=['kb:NVDA+I'])
    def script_speakParent(self, gesture):
        count=scriptHandler.getLastScriptRepeatCount()
        # Translators: error message if parent couldn't be found)
        errorMsg = _("No parent item in this tree view")
        self.moveInTree(-1, errorMsg, unbounded=True, op=operator.lt, speakOnly=True, moveCount=count+1)

    @script(description="Moves to the next child in tree view.", gestures=['kb:NVDA+alt+RightArrow'])
    def script_moveToChild(self, gesture):
        # Translators: error message if a child couldn't be found
        errorMsg = _("NO child")
        self.moveInTree(1, errorMsg, unbounded=False, op=operator.gt)

    @script(description="Moves to parent in tree view.", gestures=['kb:NVDA+alt+LeftArrow'])
    def script_moveToParent(self, gesture):
        # Translators: error message if parent couldn't be found
        errorMsg = _("No parent")
        self.moveInTree(-1, errorMsg, unbounded=True, op=operator.lt)

    def getLevel(self, obj):
        try:
            return obj.positionInfo["level"]
        except AttributeError:
            return None
        except KeyError:
            return None


    def moveInTree(self, increment, errorMessage, unbounded=False, op=operator.eq, speakOnly=False, moveCount=1):
        obj = api.getFocusObject()
        level = self.getLevel(obj)
        found = False
        levels = []
        while True:
            if increment > 0:
                obj = obj.next
            else:
                obj = obj.previous
            newLevel = self.getLevel(obj)
            if newLevel is None:
                break
            if op(newLevel, level):
                found = True
                level = newLevel
                result = obj
                moveCount -= 1
                if moveCount == 0:
                    break
            elif newLevel < level:
                # Not found in this subtree
                if not unbounded:
                    break
            levels.append(newLevel )

        if found:
            self.beeper.fancyCrackle(levels, volume=getConfig("crackleVolume"))
            if not speakOnly:
                result.setFocus()
            else:
                speech.speakObject(result)
        else:
            self.endOfDocument(errorMessage)

    def endOfDocument(self, message):
        volume = getConfig("noNextTextChimeVolume")
        self.beeper.fancyBeep("HF", 100, volume, volume)
        if getConfig("noNextTextMessage"):
            ui.message(message)
