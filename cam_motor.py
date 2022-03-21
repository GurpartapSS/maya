import RPi._GPIO as gpio
import time
class cam_motor:
    def __init__(self):
        self.gp = gpio
        self.gp.setmode(gpio.BCM)
        mode = self.gp.getmode()
        print("** GPIO Initialised for cam, Mode:", mode)
    
    def setup(self):
        self.gp.setup(12, gpio.OUT)
        self.servo = self.gp.PWM(12, 50)

        self.servo.start(0)
        self.servo.ChangeDutyCycle(7)
        time.sleep(.2)
        self.servo.ChangeDutyCycle(0)
        print("waiting")

    def rotate(self,PWM):
        self.servo.ChangeDutyCycle(PWM)
        time.sleep(.05)
        self.servo.ChangeDutyCycle(0)
        time.sleep(.05)

    def __del__(self):
        self.servo.stop()
        self.gp.cleanup()
