import speech_recognition as sr
import wakeUp_detect

class audioRec:
    def __init__(self):
        self.__r = sr.Recognizer()

    def getText(self):
        global text
        with sr.Microphone() as source:
            print("Listening..")
            audio = self.__r.listen(source)

        try:
            text = self.__r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

#test
# if __name__ == '__main__':
#     ad = wakeUp_detect.HotWord()
#     check = ad.getKeyword()
#     del ad
#     if(check == 0):
#         r= audioRec()
#         text = None
#         text = r.getText()
#         if text is not None:
#             print(f"Recognized: {text}")
#         else:
#             print("Unable to get command")
#         del r

