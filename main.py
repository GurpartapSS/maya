#start bot server and wait for connection and override signal (Key combination)
# import botServer

import wakeUp_detect
import audioDetection
import faceDetection_coral as fd

if __name__ == "__main__":
    print("Starting main ..")
    state = 1
    __hotWord = wakeUp_detect.HotWord()
    __audioStr = audioDetection.audioRec()
    listening = False
    while(1):
        if state == 1:
            wake_up = __hotWord.getKeyword()
            if wake_up == 0:
                state = 2
        if state == 2:
            text = None
            text = __audioStr.getText()
            if text is not None:
                print(f"Recognized: {text}")
                if "Stop".lower() in text.lower():
                    print("stopping stream!")
                    state = 0
                if "Sleep".lower() in text.lower():
                    print("back to hotword detection")
                    state = 1 
                if "follow me".lower() in text.lower():
                    f = fd.faceCoral()
                    f.detectFace_AND_apply_boundingBox()
            else:
                print("Unable to get command")
        if state == 0:
            del __hotWord
            del __audioStr
            break