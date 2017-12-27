
# This addon allows to navigate documents by indentation or offset level.
# In browsers you can navigate by object location on the screen.
# In editable text fields you can navigate by the indentation level.
# This is useful for editing source code.
# Author: Tony Malykh <anton.malykh@gmail.com>
# https://github.com/mltony/nvda-indent-nav/ 
# Original author: Sean Mealin <spmealin@gmail.com>

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


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    MY_LOG_NAME = "C:\\Users\\tony\\1.txt" 
    open(MY_LOG_NAME, "w").close()
    
    def mylog(self, s):
        f = open(self.MY_LOG_NAME, "a")
        f.write(str(s))
        f.write("\n")        
        f.close()
    
    def describe(self, obj):
        self.mylog(str(obj))
        self.mylog(str(type(obj)))
        for s in dir(obj):
            self.mylog("." + str(s))
        

    def isEmptyLine(self, s):
        return len(s.strip().strip("\n\r")) == 0
        
    def getIndentLevel(self, s):
        if self.isEmptyLine(s):
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
        self.moveToSibling(1, "No next line within indentation block")

    def script_moveToNextSiblingForce(self, gesture):
        self.moveToSibling(1, "No next line in the document", True)
    
    def script_moveToPreviousSibling(self, gesture):
        self.moveToSibling(-1, "No previous line within indentation block")
    def script_moveToPreviousSiblingForce(self, gesture):
        self.moveToSibling(-1, "No previous line in the document", True)
        
    script_moveToNextSibling.__doc__ = "Moves to the next line with the same indentation level as the current line within the current indentation block."
    script_moveToNextSiblingForce.__doc__ = "Moves to the next line with the same indentation level as the current line potentially in the following indentation block."

    
    script_moveToPreviousSibling.__doc__ = "Moves to the previous line with the same indentation level as the current line within the current indentation block."
    script_moveToPreviousSiblingForce.__doc__ = "Moves to the previous line with the same indentation level as the current line within the current indentation block."
    
    def moveToSibling(self, increment, errorMessage, unbounded=False, op=operator.eq):
        self.mylog("%d %s" % (increment, str(unbounded)))
        focus = api.getFocusObject()
        if focus.role == controlTypes.ROLE_EDITABLETEXT:
            self.moveToSiblingInEditable(increment, errorMessage, unbounded, op)
        else:
            self.moveToSiblingInBrowser(increment, errorMessage, op)


    def moveToSiblingInEditable(self, increment, errorMessage, unbounded=False, op=operator.eq): 
        focus = api.getFocusObject()
        # Get the current indentation level 
        textInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
        textInfo.expand(textInfos.UNIT_LINE)
        indentationLevel = self.getIndentLevel(textInfo.text)
        onEmptyLine = self.isEmptyLine(textInfo.text) == 1  # 1 because an empty line will have the \n character
        
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
            if not onEmptyLine and self.isEmptyLine(textInfo.text):
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

    def moveToSiblingInBrowser(self, increment, errorMessage, op):
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
        self.moveToSibling(1, "No child block within indentation block", unbounded=False, op=operator.gt)

    script_moveToChild.__doc__ = "Moves to the next line with a greater indentation level than the current line within the current indentation block."
    
    def script_moveToParent(self, gesture):
        self.moveToSibling(-1, "No parent of indentation block", unbounded=True, op=operator.lt)

    script_moveToParent.__doc__ = "Moves to the previous line with a lesser indentation level than the current line within the current indentation block."
    
    __gestures = {
        "kb:NVDA+alt+DownArrow": "moveToNextSibling",
        "kb:NVDA+alt+control+DownArrow": "moveToNextSiblingForce",
        "kb:NVDA+alt+UpArrow": "moveToPreviousSibling",
        "kb:NVDA+alt+control+UpArrow": "moveToPreviousSiblingForce",
        "kb:NVDA+alt+LeftArrow": "moveToParent",
        "kb:NVDA+alt+RightArrow": "moveToChild"
    }
pass
