import os
import speech_recognition as sr
import wakeUp_detect
import run_model

class audioRec:
    def __init__(self):
        self.__r = sr.Recognizer()

    def getText(self):
        global text
        with sr.Microphone() as source:
            print("Listening for command ...")
            audio = self.__r.listen(source, timeout= 5)

        try:
            text = self.__r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

## Test -- adding state machine to determine which audio to open
# 0 - stop listening
# 1 - listening for hotword offline
# 2 - listening for comand -- google API
if __name__ == '__main__':
    state = 1
    __hotWord = None
    # __audioStr = audioRec()
    listening = False
    while(1):
        if state == 1:
            if __hotWord is None:
                __hotWord = wakeUp_detect.HotWord()
            wake_up = __hotWord.getKeyword()
            if wake_up == 0:
                state = 2
        if state == 2:
            # text = None
            # text = __audioStr.getText()
            # if text is not None:
            #     print(f"Recognized: {text}")
            #     if "Stop".lower() in text.lower():
            #         print("stopping stream!")
            #         state = 0
            #     if "Sleep".lower() in text.lower():
            #         print("back to hotword detection")
            #         state = 1 
            # else:
            run_model.main()
            #     print("Unable to get command")
            # break
        if state == 0:
            del __hotWord
            # del __audioStr
            break

