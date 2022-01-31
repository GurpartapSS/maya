import RPi.GPIO as gpio
import time

class actuator:
    def __init__(self):
        self.gpio = gpio
        #define the GPIO pins that we will use 
        self.__RL_F = 5    #RL-F --> Rear_Left_Forward
        self.__RL_R = 6
        self.__RR_R = 13
        self.__RR_F = 19
        self.__FL_R = 12
        self.__FL_F = 16
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
        self.channel_Turn = (self.__RL_F,self.__RR_R,self.__FL_F,self.__FR_R)

    def __del__(self):
        self.gpio.cleanup()

    def setup_gpio(self):
        try:
            self.gpio.setmode(gpio.BCM)
            mode = self.gpio.getmode()
            print("** GPIO Initialised Mode:", mode)
            self.gpio.setup(self.channel_list, gpio.OUT, initial = gpio.LOW)
        except:
            print("** Unable to initialise gpio")


    #define movement, if in automode, will move at default speed
    #if in manual mode, speed depends on the controller intensity
    def movement_auto(self,direction):
        if(direction == "up"):
            print("** Moving Forward")
            # self.gpio.output(self.channel_forward, gpio.HIGH)
        elif(direction == "back"):
            # self.gpio.output(self.channel_rev, gpio.HIGH)
            print("** Moving Reverse")
        elif(direction == "left"):
            print("** Moving left")
        elif(direction == "right"):
            print("** Moving right")
        elif(direction == "rotate_left"):
            print("** Turning Left")
        elif(direction == "rotate_right"):
            print("** Turning Right")
        elif(direction == "right_up"):
            print("** Going Right up")

    def movement_controlled(direction, intensity):
        print("**** Not implemented!")

    def movement_stop(self):
        self.gpio.output(self.channel_list, gpio.LOW)


# setup_gpio()
# movement_auto("back")
# # time.sleep(1)
# movement_stop()
# time.sleep(1)
# movement_auto("up")
# # time.sleep(1)
# movement_stop()
# gpio_clean()

# t = actuator()
# t.setup_gpio()
# t.movement_auto("up")
# del t
