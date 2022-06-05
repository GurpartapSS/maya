import RPi.GPIO as gpio
import time
from constants import directions

class actuator:
    def __init__(self):
        self.gpio = gpio
        self.dir = directions()
        #define the GPIO pins that we will use 
        self.__RL_F = 5    #RL-F --> Rear_Left_Forward
        self.__RL_R = 6
        self.__RR_R = 19
        self.__RR_F = 13
        self.__FL_R = 16
        self.__FL_F = 26
        self.__FR_F = 20
        self.__FR_R = 21

        self.channel_list = (self.__RL_F,self.__RL_R,self.__RR_R,self.__RR_F,self.__FL_R,self.__FL_F,self.__FR_F,self.__FR_R)
        self.channel_forward = (self.__RL_F,self.__RR_F,self.__FL_F,self.__FR_F)
        self.channel_rev = (self.__RL_R,self.__RR_R,self.__FL_R,self.__FR_R)
        self.channel_right = (self.__RR_R,self.__RL_F,self.__FL_R,self.__FR_F)
        self.channel_left = (self.__FL_F,self.__FR_R,self.__RL_R,self.__RR_F)
        self.channel_Rup = (self.__FR_F,self.__RL_F)
        self.channel_Lup = (self.__FL_F,self.__RR_F)
        self.channel_Rdown = (self.__FL_R,self.__RR_R)
        self.channel_Ldown = (self.__FR_R,self.__RL_R)
        self.channel_RTurn = (self.__RL_F,self.__RR_R,self.__FL_F,self.__FR_R)
        self.channel_LTurn = (self.__RL_F,self.__RR_R,self.__FL_F,self.__FR_R)


    def __del__(self):
        self.gpio.cleanup()

    def setup_gpio(self):
        try:
            self.gpio.setmode(gpio.BCM)
            mode = self.gpio.getmode()
            print("** GPIO Initialised Mode:", mode)
            self.gpio.setup(self.channel_list, gpio.OUT, initial = gpio.LOW)
            self.gpio.setup(12,self.gpio.OUT)
            self.pwm = self.gpio.PWM(12, 100)
            self.pwm.start(50)
        except:
            print("** Unable to initialise gpio")


    #define movement, if in automode, will move at default speed
    #if in manual mode, speed depends on the controller intensity
    def movement_auto(self,direction):
        if(direction == self.dir.FORW):
            print("** Moving Forward")
            self.gpio.output(self.channel_forward, gpio.HIGH)
        elif(direction == self.dir.BACK):
            print("** Moving Reverse")
            self.gpio.output(self.channel_rev, gpio.HIGH)
        elif(direction == self.dir.LEFT):
            print("** Moving left")
            self.gpio.output(self.channel_left, gpio.HIGH)
        elif(direction == self.dir.RIGHT):
            print("** Moving right")
            self.gpio.output(self.channel_right, gpio.HIGH)
        elif(direction == self.dir.ROT_LEFT):
            print("** Turning Left")
            self.gpio.output(self.channel_LTurn, gpio.HIGH)
        elif(direction == self.dir.ROT_RIGHT):
            print("** Turning Right")
            self.gpio.output(self.channel_RTurn, gpio.HIGH)
        elif(direction == self.dir.RIGHT_UP):
            print("** Going Right up")
            self.gpio.output(self.channel_Rup, gpio.HIGH)

    def movement_controlled(direction, intensity):
        print("**** Not implemented!")

    def movement_stop(self):
        print("**** Stopped")
        self.gpio.output(self.channel_list, gpio.LOW)
        time.sleep(.2)

# Test
    def test(self):
        # t = actuator()
        # t.setup_gpio()
        self.movement_stop()
        self.movement_auto(1)
        time.sleep(1)
        self.movement_stop()
        # del t

# if __name__ == "__main__":
#     t= actuator()
#     t.setup_gpio()
#     i = 0
#     while(i < 4):
#         t.test()
#         time.sleep(1)
#         i = i+1;
