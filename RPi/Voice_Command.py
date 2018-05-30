import os, sys
import speech_recognition as sr

class Voice_Command():
    
    def __init__(self, ir_transceiver):
        # Object definitions
        self.ir_transceiver = ir_transceiver
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        # Load commands from file
        self.loadConfig()
        # Adjust sensitivity for background noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        # Start listening
        self.recognizer.listen_in_background(self.microphone, self.speechToText)

    def loadConfig(self):
        self.commandList = {}
        file_cfg = open(os.path.join(sys.path[0], 'voice_command.cfg'), 'r')
        if (file_cfg):
            for line in file_cfg:
                command = line.split(';')
                self.commandList[command[0]] = command[1]
            file_cfg.close()

    def saveConfig(self):
        file_cfg = open(os.path.join(sys.path[0], 'voice_command.cfg'), 'w')
        if (file_cfg):
            for key, value in self.commandList.items():
                print >>file_cfg, ('%s;%s' % (key, value))
            file_cfg.close()

    def speechToText(self, r, audio):
        try:
            phrase = r.recognize_google(audio)
            ir_code = self.commandList[phrase]
            self.ir_transceiver.sendIR(ir_code)
            return True
        except:
            return False

    def addCommand(self, command, ir_code):
        # Check if command is already included in list
        inList = False
        for key in self.commandList:
            if key.lower() == command.lower().strip():
                inList = True
        if not inList:
            self.commandList[command.strip()] = ir_code
            self.saveConfig()
            return True
        else:
            return False

    def removeCommand(self, command):
        # Ensure command is included in list
        inList = False
        for key in self.commandList:
            if key.lower() == command.lower().strip():
                inList = True
        if inList:
            del self.commandList[command]
            self.saveConfig()
            return True
        else:
            return False
    
