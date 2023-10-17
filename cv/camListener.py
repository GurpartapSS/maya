import RPi._GPIO as gpio
import time
class cam_motor:
    def __init__(self):
        self.gp = gpio
        self.gp.setmode(gpio.BCM)
        mode = self.gp.getmode()
        self.__PMW = 7
        print("** GPIO Initialised for cam, Mode:", mode)
    
    def setup(self):
        self.gp.setup(12, gpio.OUT)
        self.servo = self.gp.PWM(12, 50)

        self.servo.start(0)
        self.servo.ChangeDutyCycle(self.__PMW)
        time.sleep(.2)
        self.servo.ChangeDutyCycle(0)
        print("waiting for motion in cam ..")

    def rotate(self,motion):
        self.__PMW = self.__PMW + motion
        print("now PWM ..",self.__PMW)
        self.servo.ChangeDutyCycle(self.__PMW)
        time.sleep(.1)
        self.servo.ChangeDutyCycle(0)
        time.sleep(.1)

    def __del__(self):
        self.servo.stop()
        self.gp.cleanup()
