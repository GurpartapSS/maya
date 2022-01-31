import RPi.GPIO as gpio
import time

#define the GPIO pins that we will use 
M1P1 = 5
M1P2 = 6
M2P1 = 13
M2P2 = 19
M3P1 = 12
M3P2 = 16
M4P1 = 20
M4P2 = 21

channel_list = (M1P1,M1P2,M2P1,M2P2,M3P1,M3P2,M4P1,M4P2)
channel_forward = (M1P1,M2P2,M3P2,M4P1)
channel_rev = (M1P2,M2P1,M3P1,M4P2)
channel_left = (M1P2,M2P1,M3P1,M4P2)
channel_right = (M1P2,M2P1,M3P1,M4P2)


class actuator:
    def __init__(self):
        self.gpio = gpio

    def __del__(self):
        self.gpio.cleanup()

    def setup_gpio(self):
        try:
            self.gpio.setmode(gpio.BCM)
            mode = self.gpio.getmode()
            print("** GPIO Initialised")

            self.gpio.setup(channel_list, gpio.OUT, initial = gpio.LOW)
        except:
            print("** Unable to initialise gpio")


    #define movement, if in automode, will move at default speed
    #if in manual mode, speed depends on the controller intensity
    def movement_auto(self,direction):
        if(direction == "up"):
            print("** Moving Forward")
            self.gpio.output(channel_forward, gpio.HIGH)
        elif(direction == "back"):
            self.gpio.output(channel_rev, gpio.HIGH)
            print("** Moving Reverse")
        elif(direction == "left"):
            print("** Moving left")
        elif(direction == "right"):
            print("** Moving right")
        elif(direction == "rotate_left"):
            print("** Turning Left")
        elif(direction == "rotate_right"):
            print("** Turning Right")

    def movement_controlled(direction, intensity):
        print("**** Not implemented!")

    def movement_stop(self):
        self.gpio.output(channel_list, gpio.LOW)


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
