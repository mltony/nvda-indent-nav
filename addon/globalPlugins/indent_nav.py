#A part of the IndentNav addon for NVDA
#Copyright (C) 2017-2018 Tony Malykh
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
import ctypes
import globalPluginHandler
import gui
import NVDAHelper
import operator
import re
import scriptHandler
from scriptHandler import script
import speech
import struct
import textInfos
import tones
import ui
import wx

def myAssert(condition):
    if not condition:
        raise RuntimeError("Assertion failed")


def createMenu():
    def _popupMenu(evt):
        gui.mainFrame._popupSettingsDialog(SettingsDialog)
    prefsMenuItem  = gui.mainFrame.sysTrayIcon.preferencesMenu.Append(wx.ID_ANY, _("IndentNav..."))
    gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, _popupMenu, prefsMenuItem)

def initConfiguration():
    confspec = {
        "crackleVolume" : "integer( default=25, min=0, max=100)",
        "noNextTextChimeVolume" : "integer( default=50, min=0, max=100)",
        "noNextTextMessage" : "boolean( default=False)",
        "browserMode" : "integer( default=0, min=0, max=2)",
        "useFontFamily" : "boolean( default=True)",
        "useColor" : "boolean( default=True)",
        "useBackgroundColor" : "boolean( default=True)",
    }
    config.conf.spec["indentnav"] = confspec

def getConfig(key):
    value = config.conf["indentnav"][key]
    return value

def setConfig(key, value):
    config.conf["indentnav"][key] = value


addonHandler.initTranslation()
initConfiguration()
createMenu()


class SettingsDialog(gui.SettingsDialog):
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

        # Translators: Checkbox that controls whether font family should be used for style
        label = _("Use font family for style")
        self.useFontFamilyCheckBox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.useFontFamilyCheckBox.Value = getConfig("useFontFamily")

        # Translators: Checkbox that controls whether font color should be used for style
        label = _("Use font color for style")
        self.useColorCheckBox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.useColorCheckBox.Value = getConfig("useColor")

        # Translators: Checkbox that controls whether background color should be used for style
        label = _("Use background color for style")
        self.useBackgroundColorCheckBox = sHelper.addItem(wx.CheckBox(self, label=label))
        self.useBackgroundColorCheckBox.Value = getConfig("useBackgroundColor")

    def onOk(self, evt):
        config.conf["indentnav"]["crackleVolume"] = self.crackleVolumeSlider.Value
        config.conf["indentnav"]["noNextTextChimeVolume"] = self.noNextTextChimeVolumeSlider.Value
        config.conf["indentnav"]["noNextTextMessage"] = self.noNextTextMessageCheckbox.Value
        config.conf["indentnav"]["useFontFamily"] = self.useFontFamilyCheckBox.Value
        config.conf["indentnav"]["useColor"] = self.useColorCheckBox.Value
        config.conf["indentnav"]["useBackgroundColor"] = self.useBackgroundColorCheckBox.Value
        super(SettingsDialog, self).onOk(evt)

# Browse mode constants:
BROWSE_MODES = [
    _("horizontal offset"),
    _("font size"),
    _("font size and same style"),
]

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("IndentNav")



    def getIndentLevel(self, s):
        if speech.isBlank(s):
            return 0
        indent = speech.splitTextIndentation(s)[0]
        return len(indent.replace("\t", " " * 4))

    def uniformSample(self, a, m):
        n = len(a)
        if n <= m:
            return a
        # Here assume n > m
        result = []
        for i in xrange(0, m*n, n):
            result.append(a[i  / m])
        return result

    BASE_FREQ = speech.IDT_BASE_FREQUENCY
    def getPitch(self, indent):
        return self.BASE_FREQ*2**(indent/24.0) #24 quarter tones per octave.

    BEEP_LEN = 10 # millis
    PAUSE_LEN = 5 # millis
    MAX_CRACKLE_LEN = 400 # millis
    MAX_BEEP_COUNT = MAX_CRACKLE_LEN / (BEEP_LEN + PAUSE_LEN)

    def crackle(self, levels):
        if self.isReportIndentWithTones():
            self.fancyCrackle(levels, volume=getConfig("crackleVolume"))
        else:
            self.simpleCrackle(len(levels), volume=getConfig("crackleVolume"))

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
        result = [0] * (bufSize/intSize)
        for freq in freqs:
            buf = ctypes.create_string_buffer(bufSize)
            NVDAHelper.generateBeep(buf, freq, beepLen, right, left)
            bytes = bytearray(buf)
            unpacked = struct.unpack("<%dQ" % (bufSize / intSize), bytes)
            result = map(operator.add, result, unpacked)
        maxInt = 1 << (8 * intSize)
        result = map(lambda x : x %maxInt, result)
        packed = struct.pack("<%dQ" % (bufSize / intSize), *result)
        tones.player.feed(packed)



    def isReportIndentWithTones(self):
        return config.conf["documentFormatting"]["reportLineIndentationWithTones"]

    @script(description="Moves to the next line with the same indentation level as the current line within the current indentation block.", gestures=['kb:NVDA+alt+DownArrow'])
    def script_moveToNextSibling(self, gesture):
        # Translators: error message if next sibling couldn't be found (in editable control or in browser)
        msgEditable = _("No next line within indentation block")
        msgBrowser = _("No next paragraph with the same {modeDescription} in the document")
        self.move(1, [msgEditable,msgBrowser])

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
        msgBrowser = _("No previous paragraph with the same {modeDescription} in the document")
        self.move(-1, [msgEditable, msgBrowser])

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
        if hasattr(focus, "treeInterceptor") and hasattr(focus.treeInterceptor, "makeTextInfo"):
            # We must be in browser
            mode = getConfig("browserMode")
            mode = (mode + 1) % len(BROWSE_MODES)
            setConfig("browserMode", mode)
            ui.message("IndentNav navigates by " + BROWSE_MODES[mode])
            return
        count=scriptHandler.getLastScriptRepeatCount()
        # Translators: error message if parent couldn't be found (in editable control or in browser)
        msgEditable = _("No parent of indentation block")
        msgBrowser = _("No previous paragraph with smaller offset in the document")
        self.move(-1, [msgEditable, msgBrowser], unbounded=True, op=operator.lt, speakOnly=True, moveCount=count+1)

    def generateBrowseModeExtractors(self):
        def getFontSize(textInfo, formatting):
            try:
                size =float( formatting["font-size"].replace("pt", ""))
                return size
            except:
                return 0
        mode = getConfig("browserMode")
        if mode == 0:
            # horizontal offset
            extractFormattingFunc = lambda x: None
            extractIndentFunc = lambda textInfo,x: textInfo.NVDAObjectAtStart.location[0]
            extractStyleFunc = lambda x,y: None
        elif mode in [1,2]:
            extractFormattingFunc = lambda textInfo: self.getFormatting(textInfo)
            extractIndentFunc = getFontSize
            if mode == 1:
                # Font size only
                extractStyleFunc = lambda textInfo, formatting: None
            else:
                # Both font fsize and style
                extractStyleFunc = lambda textInfo, formatting: self.formattingToStyle(formatting)
        return (
            extractFormattingFunc,
            extractIndentFunc,
            extractStyleFunc
        )
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
        if focus.role == controlTypes.ROLE_EDITABLETEXT:
            self.moveInEditable(increment, errorMessages[0], unbounded, op, speakOnly=speakOnly, moveCount=moveCount)
        elif (len(errorMessages) >= 2) and hasattr(focus, "treeInterceptor") and hasattr(focus.treeInterceptor, "makeTextInfo"):
            mode = getConfig("browserMode")
            errorMessage = errorMessages[1]
            if op == operator.eq:
                errorMessage = errorMessage.format(modeDescription=BROWSE_MODES[mode])
            else:
                if mode in [1,2]:
                    if increment > 0:
                        op =operator.lt
                    else:
                        op =operator.gt
                else:
                    if increment > 0:
                        op =operator.gt
                    else:
                        op =operator.lt
                if op == operator.gt:
                    qualifier = _("greater")
                else:
                    qualifier = _("smaller")
                errorMessage = errorMessage.format(
                modeDescription=BROWSE_MODES[mode],
                qualifier=qualifier)
            (
                extractFormattingFunc,
                extractIndentFunc,
                extractStyleFunc
            ) = self.generateBrowseModeExtractors()
            self.moveInBrowser(increment, errorMessage, op,
                extractFormattingFunc=extractFormattingFunc,
                extractIndentFunc=extractIndentFunc,
                extractStyleFunc=extractStyleFunc)
        else:
            errorMsg = _("Cannot move here")
            ui.message(errorMsg)

    def moveInEditable(self, increment, errorMessage, unbounded=False, op=operator.eq, speakOnly=False, moveCount=1):
        focus = api.getFocusObject()
        # Get the current indentation level
        textInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
        textInfo.expand(textInfos.UNIT_LINE)
        indentationLevel = self.getIndentLevel(textInfo.text)
        onEmptyLine = speech.isBlank(textInfo.text)

        # Scan each line until we hit the end of the indentation block, the end of the edit area, or find a line with the same indentation level
        found = False
        indentLevels = []
        while True:
            result = textInfo.move(textInfos.UNIT_LINE, increment)
            if result == 0:
                break
            textInfo.expand(textInfos.UNIT_LINE)
            newIndentation = self.getIndentLevel(textInfo.text)

            # Skip over empty lines if we didn't start on one.
            if not onEmptyLine and speech.isBlank(textInfo.text):
                continue

            if op(newIndentation, indentationLevel):
                # Found it
                found = True
                indentationLevel = newIndentation
                resultTextInfo = textInfo.copy()
                moveCount -= 1
                if moveCount == 0:
                    break
            elif newIndentation < indentationLevel:
                # Not found in this indentation block
                if not unbounded:
                    break
            indentLevels.append(newIndentation )

        if found:
            if not speakOnly:
                resultTextInfo.updateCaret()
            self.crackle(indentLevels)
            speech.speakTextInfo(resultTextInfo, unit=textInfos.UNIT_LINE)
        else:
            self.endOfDocument(errorMessage)

    def getFormatting(self, info):
        formatField=textInfos.FormatField()
        formatConfig=config.conf['documentFormatting']
        for field in info.getTextWithFields(formatConfig):
            #if isinstance(field,textInfos.FieldCommand): and isinstance(field.field,textInfos.FormatField):
            try:
                formatField.update(field.field)
            except:
                pass
        return formatField

    def formattingToStyle(self, formatting):
        result = []
        if getConfig("useFontFamily"):
            result.append(formatting.get("font-family", None))
        if getConfig("useColor"):
            result.append(formatting.get("color", None))
        if getConfig("useBackgroundColor"):
            result.append(formatting.get("background-color", None))
        return tuple(result)

    def moveInBrowser(self, increment, errorMessage, op,
        extractFormattingFunc,
        extractIndentFunc,
        extractStyleFunc):
        focus = api.getFocusObject()
        focus = focus.treeInterceptor
        textInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
        textInfo.expand(textInfos.UNIT_PARAGRAPH)
        origFormatting = extractFormattingFunc(textInfo)
        origIndent = extractIndentFunc(textInfo, origFormatting)
        origStyle = extractStyleFunc(textInfo, origFormatting)
        distance = 0
        while True:
            result =textInfo.move(textInfos.UNIT_PARAGRAPH, increment)
            if result == 0:
                return self.endOfDocument(errorMessage)
            textInfo.expand(textInfos.UNIT_PARAGRAPH)
            text = textInfo.text
            if speech.isBlank(text):
                continue
            formatting = extractFormattingFunc(textInfo)
            indent = extractIndentFunc(textInfo, formatting)
            style = extractStyleFunc(textInfo, formatting)
            if style == origStyle:
                if op(indent, origIndent):
                    textInfo.updateCaret()
                    self.simpleCrackle(distance, volume=getConfig("crackleVolume"))
                    speech.speakTextInfo(textInfo, reason=controlTypes.REASON_CARET)
                    return
            distance += 1


    @script(description="Moves to the next line with a greater indentation level than the current line within the current indentation block.", gestures=['kb:NVDA+alt+RightArrow'])
    def script_moveToChild(self, gesture):
        # Translators: error message if a child couldn't be found (in editable control or in browser)
        msgEditable = _("No child block within indentation block")
        msgBrowser = _("No next paragraph with {qualifier} {modeDescription} in the document")
        self.move(1, [msgEditable, msgBrowser], unbounded=False, op=operator.gt)

    @script(description="Moves to the previous line with a lesser indentation level than the current line within the current indentation block.", gestures=['kb:NVDA+alt+LeftArrow'])
    def script_moveToParent(self, gesture):
        # Translators: error message if parent couldn't be found (in editable control or in browser)
        msgEditable = _("No parent of indentation block")
        msgBrowser = _("No previous paragraph with {qualifier} {modeDescription} in the document")
        self.move(-1, [msgEditable, msgBrowser], unbounded=True, op=operator.lt)

    def endOfDocument(self, message):
        volume = getConfig("noNextTextChimeVolume")
        self.fancyBeep("HF", 100, volume, volume)
        if getConfig("noNextTextMessage"):
            ui.message(message)
