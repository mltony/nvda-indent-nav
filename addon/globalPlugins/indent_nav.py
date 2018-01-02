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
import NVDAHelper
import operator 
import speech
import textInfos
import tones
import ui

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
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
            self.fancyCrackle(levels)
        else:
            self.simpleCrackle(len(levels))

    def fancyCrackle(self, levels):
        levels = self.uniformSample(levels, self.MAX_BEEP_COUNT )
        beepLen = self.BEEP_LEN 
        pauseLen = self.PAUSE_LEN
        pauseBufSize = NVDAHelper.generateBeep(None,self.BASE_FREQ,pauseLen,0, 0)
        beepBufSizes = [NVDAHelper.generateBeep(None,self.getPitch(l), beepLen, 50, 50) for l in levels]
        bufSize = sum(beepBufSizes) + len(levels) * pauseBufSize
        buf = ctypes.create_string_buffer(bufSize)
        bufPtr = 0
        for l in levels:
            bufPtr += NVDAHelper.generateBeep(
                ctypes.cast(ctypes.byref(buf, bufPtr), ctypes.POINTER(ctypes.c_char)), 
                self.getPitch(l), beepLen, 50, 50)
            bufPtr += pauseBufSize # add a short pause
        tones.player.stop()
        tones.player.feed(buf.raw)

    def simpleCrackle(self, n):
        return self.fancyCrackle([0] * n)
    
    def isReportIndentWithTones(self):
        return config.conf["documentFormatting"]["reportLineIndentationWithTones"]
    
    def script_moveToNextSibling(self, gesture):
        """Moves to the next line with the same indentation level as the current line within the current indentation block."""
        # Translators: error message if next sibling couldn't be found (in editable control or in browser) 
        msgEditable = _("No next line within indentation block")
        msgBrowser = _("No next paragraph with the same offset in the document") 
        self.move(1, [msgEditable,msgBrowser])

    def script_moveToNextSiblingForce(self, gesture):
        """Moves to the next line with the same indentation level as the current line potentially in the following indentation block."""
        # Translators: error message if next sibling couldn't be found in editable control (forced command)
        msgEditable = _("No next line in the document")
        self.move(1, [msgEditable], True)
    
    def script_moveToPreviousSibling(self, gesture):
        """Moves to the previous line with the same indentation level as the current line within the current indentation block."""
        # Translators: error message if previous sibling couldn't be found (in editable control or in browser)
        msgEditable = _("No previous line within indentation block")
        msgBrowser = _("No previous paragraph with the same offset in the document") 
        self.move(-1, [msgEditable, msgBrowser])
        
    def script_moveToPreviousSiblingForce(self, gesture):
        """Moves to the previous line with the same indentation level as the current line within the current indentation block."""
        # Translators: error message if previous sibling couldn't be found in editable control (forced command)
        msgEditable = _("No previous line in the document")
        self.move(-1, [msgEditable], True)
    
    def move(self, increment, errorMessages, unbounded=False, op=operator.eq):
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
        """ 
        focus = api.getFocusObject()
        if focus.role == controlTypes.ROLE_EDITABLETEXT:
            self.moveInEditable(increment, errorMessages[0], unbounded, op)
        elif (len(errorMessages) >= 2) and hasattr(focus, "treeInterceptor") and hasattr(focus.treeInterceptor, "makeTextInfo"):  
            self.moveInBrowser(increment, errorMessages[1], op)
        else:
            errorMsg = _("Cannot move here")
            ui.message(errorMsg)

    def moveInEditable(self, increment, errorMessage, unbounded=False, op=operator.eq): 
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
                textInfo.updateCaret()
                self.crackle(indentLevels)
                speech.speakTextInfo(textInfo, unit=textInfos.UNIT_LINE)
                return
            elif newIndentation < indentationLevel:
                # Not found in this indentation block
                if not unbounded:
                    break
            indentLevels.append(newIndentation )
        
        # If we didn't find it, tell the user
        if not found:
            ui.message(errorMessage)

    def moveInBrowser(self, increment, errorMessage, op):
        focus = api.getFocusObject()
        focus = focus.treeInterceptor 
        textInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
        textInfo.expand(textInfos.UNIT_PARAGRAPH)
        origLocation= textInfo.NVDAObjectAtStart.location
        distance = 0
        while True:
            result =textInfo.move(textInfos.UNIT_PARAGRAPH, increment)
            if result == 0:
                ui.message(errorMessage)
                return
            textInfo.expand(textInfos.UNIT_PARAGRAPH)
            location = textInfo.NVDAObjectAtStart.location
            if op(location[0], origLocation[0]):
                text = textInfo.text
                textInfo.collapse(False)
                textInfo.updateCaret()
                self.simpleCrackle(distance)
                ui.message(text)
                return
            distance += 1

    def script_moveToChild(self, gesture):
        """Moves to the next line with a greater indentation level than the current line within the current indentation block."""
        # Translators: error message if a child couldn't be found (in editable control or in browser)
        msgEditable = _("No child block within indentation block")
        msgBrowser = _("No next paragraph with greater offset in the document")
        self.move(1, [msgEditable, msgBrowser], unbounded=False, op=operator.gt)

    def script_moveToParent(self, gesture):
        """Moves to the previous line with a lesser indentation level than the current line within the current indentation block."""
        # Translators: error message if parent couldn't be found (in editable control or in browser)
        msgEditable = _("No parent of indentation block")
        msgBrowser = _("No previous paragraph with smaller offset in the document")
        self.move(-1, [msgEditable, msgBrowser], unbounded=True, op=operator.lt)
        
    __gestures = {

        "kb:NVDA+alt+DownArrow": "moveToNextSibling",
        "kb:NVDA+alt+control+DownArrow": "moveToNextSiblingForce",
        "kb:NVDA+alt+UpArrow": "moveToPreviousSibling",
        "kb:NVDA+alt+control+UpArrow": "moveToPreviousSiblingForce",
        "kb:NVDA+alt+LeftArrow": "moveToParent",
        "kb:NVDA+alt+RightArrow": "moveToChild"
    }
