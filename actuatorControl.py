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

# def setup_gpio():
    # try:
gpio.setmode(gpio.BCM)
mode = gpio.getmode()
print("** GPIO Initialised")

gpio.setchannel(channel_list, gpio.OUT, initial = gpio.LOW)
    # except:
        # print("** Unable to initialise gpio")


#define movement, if in automode, will move at default speed
#if in manual mode, speed depends on the controller intensity
def movement_auto(direction):
    if(direction == "up"):
        print("** Moving Forward")
        gpio.output(channel_forward, gpio.HIGH)
        # gpio.output(M1P1, gpio.HIGH)
        # gpio.output(M1P1, gpio.HIGH)
        # gpio.output(M1P1, gpio.HIGH)
        # gpio.output(M1P1, gpio.HIGH)
    elif(direction == "back"):
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
    if(direction == "up"):
        print("** Moving Forward at intensity ", intensity)
        gpio.output(M1P1, gpio.HIGH)
        gpio.output(M1P1, gpio.HIGH)
        gpio.output(M1P1, gpio.HIGH)
        gpio.output(M1P1, gpio.HIGH)

def movement_stop():
    gpio(channel_list, gpio.LOW)

# setup_gpio()
# movement_auto("up")
gpio.output(M4P1, gpio.HIGH) # for left back forward 
gpio.output(M4P2, gpio.LOW) #for right back back # for left forward back # for right forward for
time.sleep(2)
movement_stop()
gpio.cleanup()
