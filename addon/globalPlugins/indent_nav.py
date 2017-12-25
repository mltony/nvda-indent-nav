
# This plugin allows NVDA to navigate by indentation level.
# This means for whitespace-sensitive text, such as Python code, you can jump over entire blocks with one keystroke.
# Sean Mealin <spmealin@gmail.com>

import api
import controlTypes
import ctypes
import globalPluginHandler
from NVDAHelper import generateBeep
import speech
import textInfos
import tones
import ui
from logHandler import log


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
    
    def script_moveToPreviousSibling(self, gesture):
        self.moveToSibling(-1, "No previous line within indentation block")
    
    def moveToSibling(self, increment, errorMessage, force=False):
        # Make sure we're in a editable control
        focus = api.getFocusObject()
        #self.describe(focus)
        self.mylog(focus.basicText)
        #self.mylog(focus.next.basicText)
        #self.mylog(focus.previous.basicText)
        self.mylog(focus.location)
        self.mylog(focus.locationText)
        self.mylog("hahaha")
        focus = focus.treeInterceptor 
        #self.describe(focus)
        ft = focus.makeTextInfo(textInfos.POSITION_CARET)
        ft.expand(textInfos.UNIT_PARAGRAPH)
        ft.move(textInfos.UNIT_PARAGRAPH, 1)
        ft.expand(textInfos.UNIT_PARAGRAPH)
        self.mylog(ft.text)
        self.mylog(ft.pointAtStart.x)
        self.mylog(ft.locationText)
        #self.describe(ft)
        ft.updateCaret()
        ft.expand(textInfos.UNIT_PARAGRAPH)
        ui.message(ft.text)
        return
        
        if focus.role != controlTypes.ROLE_EDITABLETEXT:
            ui.message("Not in an edit control.")
            return
        
        # Get the current indentation level 
        #textInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
        textInfo = focus.makeTextInfo(textInfos.POSITION_CARET)
        textInfo.expand(textInfos.UNIT_LINE)
        indentationLevel = self.getIndentLevel(textInfo.text)
        self.mylog("inc=%d, text=%s" % (increment, textInfo.text.rstrip("\r\n")))
        for s in dir(textInfo):
            pass
            #self.mylog("%s" % str(s))
        #self.mylog("%s" % str(dir(textInfo)))
        onEmptyLine = self.isEmptyLine(textInfo.text) == 1  # 1 because an empty line will have the \n character
        
        # Scan each line until we hit the end of the indentation block, the end of the edit area, or find a line with the same indentation level
        found = False
        indentLevels = []
        while True:
            errCode = textInfo.move(textInfos.UNIT_LINE, increment) 
            if errCode  == 0:
                self.mylog("Cannot move by increment errCode=%d" % errCode)
                break
            textInfo.expand(textInfos.UNIT_LINE)
            self.mylog("inc=%d, text=%s" % (increment, textInfo.text.rstrip("\r\n")))
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
                break
            elif newIndentation < indentationLevel:
                # Not found in this indentation block
                if not force:
                    break
            indentLevels.append(newIndentation )
        
        # If we didn't find it, tell the user
        if not found:
            ui.message(errorMessage)

    script_moveToNextSibling.__doc__ = "Moves to the next line with the same indentation level as the current line within the current indentation block."
    
    script_moveToPreviousSibling.__doc__ = "Moves to the previous line with the same indentation level as the current line within the current indentation block."
    
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
        "kb:NVDA+control+alt+downArrow": "moveToNextSibling",
        "kb:NVDA+control+alt+upArrow": "moveToPreviousSibling",
        "kb:NVDA+control+alt+leftArrow": "moveToParent",
        "kb:NVDA+control+alt+rightArrow": "moveToChild"
    }
pass
