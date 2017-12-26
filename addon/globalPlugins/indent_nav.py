
# This addon allows to navigate documents by indentation or offset level.
# In browsers you can navigate by object location on the screen.
# In editable text fields you can navigate by the indentation level.
# This is useful for editing source code.
# Author: Tony Malykh <anton.malykh@gmail.com>
# https://github.com/mltony/nvda-indent-nav/ 
# Original author: Sean Mealin <spmealin@gmail.com>

import api
import controlTypes
import ctypes
import globalPluginHandler
from NVDAHelper import generateBeep
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
    PAUSE_LEN = 2 # millis
    MAX_CRACKLE_LEN = 400 # millis
    MAX_BEEP_COUNT = MAX_CRACKLE_LEN / (BEEP_LEN + PAUSE_LEN)
    def crackle(self, levels):
        levels = self.uniformSample(levels, self.MAX_BEEP_COUNT )
        beepLen = self.BEEP_LEN 
        pauseLen = self.PAUSE_LEN
        pauseBufSize = generateBeep(None,self.BASE_FREQ,pauseLen,0, 0)
        beepBufSizes = [generateBeep(None,self.getPitch(l), beepLen, 50, 50) for l in levels]
        bufSize = sum(beepBufSizes) + len(levels) * pauseBufSize
        buf = ctypes.create_string_buffer(bufSize)
        bufPtr = 0
        for l in levels:
            bufPtr += generateBeep(
                ctypes.cast(ctypes.byref(buf, bufPtr), ctypes.POINTER(ctypes.c_char)), 
                self.getPitch(l), beepLen, 50, 50)
            bufPtr += pauseBufSize # add a short pause
        tones.player.stop()
        tones.player.feed(buf.raw)
    
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
    
    def moveToSibling(self, increment, errorMessage, force=False):
        self.mylog("%d %s" % (increment, str(force)))
        self.mylog("%d %s" % (increment, str(force)))
        focus = api.getFocusObject()
        if focus.role == controlTypes.ROLE_EDITABLETEXT:
            return self.moveToSiblingInEditable(increment, errorMessage, force)
        else:
            return self.moveToSiblingInBrowser(increment, errorMessage)


    def moveToSiblingInEditable(self, increment, errorMessage, force=False): 
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
            errCode = textInfo.move(textInfos.UNIT_LINE, increment) 
            if errCode  == 0:
                break
            textInfo.expand(textInfos.UNIT_LINE)
            newIndentation = self.getIndentLevel(textInfo.text)
            
            # Skip over empty lines if we didn't start on one.
            if not onEmptyLine and self.isEmptyLine(textInfo.text):
                continue
            
            if newIndentation == indentationLevel:
                # Found it
                found = True
                textInfo.updateCaret()
                self.crackle(indentLevels)
                speech.speakTextInfo(textInfo, unit=textInfos.UNIT_LINE)
                return
            elif newIndentation < indentationLevel:
                # Not found in this indentation block
                if not force:
                    break
            indentLevels.append(newIndentation )
        
        # If we didn't find it, tell the user
        if not found:
            ui.message(errorMessage)
            
    def moveToSiblingInBrowser(self, increment, errorMessage):
        focus = api.getFocusObject()
        focus = focus.treeInterceptor 
        textInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
        textInfo.expand(textInfos.UNIT_PARAGRAPH)
        origLocation= textInfo.NVDAObjectAtStart.location
        while True:
            result =textInfo.move(textInfos.UNIT_PARAGRAPH, increment)
            if result == 0:
                ui.message(errorMessage)
                return
            textInfo.expand(textInfos.UNIT_PARAGRAPH)
            location = textInfo.NVDAObjectAtStart.location
            if location[0] == origLocation[0]:
                text = textInfo.text
                textInfo.collapse(False)
                textInfo.updateCaret()
                ui.message(text)
                return

    def script_moveToChild(self, gesture):
        # Make sure we're in a editable control
        focus = api.getFocusObject()
        if focus.role != controlTypes.ROLE_EDITABLETEXT:
            ui.message("Not in an edit control.")
            return
        
        # Get the current indentation level 
        textInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
        textInfo.expand(textInfos.UNIT_LINE)
        indentationLevel = len(textInfo.text) - len(textInfo.text.strip())
        onEmptyLine = len(textInfo.text) == 1  # 1 because an empty line will have the \n character
        
        # Scan each line until we hit the end of the indentation block, the end of the edit area, or find a line with grater indentation level
        found = False
        while textInfo.move(textInfos.UNIT_LINE, 1) == 1:
            textInfo.expand(textInfos.UNIT_LINE)
            newIndentation = len(textInfo.text) - len(textInfo.text.strip())
            
            # Skip over empty lines if we didn't start on one.
            if not onEmptyLine and len(textInfo.text) == 1:
                continue
            
            if newIndentation > indentationLevel:
                # Found it
                found = True
                textInfo.updateCaret()
                speech.speakTextInfo(textInfo, unit=textInfos.UNIT_LINE)
                break
            elif newIndentation < indentationLevel:
                # Not found in this indentation block
                break
        
        # If we didn't find it, tell the user
        if not found:
            ui.message("No child block within indentation block")

    script_moveToChild.__doc__ = "Moves to the next line with a greater indentation level than the current line within the current indentation block."
    
    def script_moveToParent(self, gesture):
        # Make sure we're in a editable control
        focus = api.getFocusObject()
        if focus.role != controlTypes.ROLE_EDITABLETEXT:
            ui.message("Not in an edit control.")
            return
        
        # Get the current indentation level 
        textInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
        textInfo.expand(textInfos.UNIT_LINE)
        indentationLevel = len(textInfo.text) - len(textInfo.text.strip())
        onEmptyLine = len(textInfo.text) == 1  # 1 because an empty line will have the \n character
        
        # Scan each line until we hit the start of the indentation block, the start of the edit area, or find a line with less indentation level
        found = False
        while textInfo.move(textInfos.UNIT_LINE, -2) == -2:
            textInfo.expand(textInfos.UNIT_LINE)
            newIndentation = len(textInfo.text) - len(textInfo.text.strip())
            
            # Skip over empty lines if we didn't start on one.
            if not onEmptyLine and len(textInfo.text) == 1:
                continue
            
            if newIndentation < indentationLevel:
                # Found it
                found = True
                textInfo.updateCaret()
                speech.speakTextInfo(textInfo, unit=textInfos.UNIT_LINE)
                break
        
        # If we didn't find it, tell the user
        if not found:
            ui.message("No parent of indentation block")

    script_moveToParent.__doc__ = "Moves to the previous line with a lesser indentation level than the current line within the current indentation block."
    
    __gestures = {
        "kb:NVDA+alt+DownArrow": "moveToNextSibling",
        "kb:NVDA+alt+control+DownArrow": "moveToNextSiblingForce",
        "kb:NVDA+alt+UpArrow": "moveToPreviousSibling",
        "kb:NVDA+alt+control+UpArrow": "moveToPreviousSiblingForce",
        "kb:NVDA+shift+numpad4": "moveToParent",
        "kb:NVDA+shift+numpad6": "moveToChild"
    }
pass
