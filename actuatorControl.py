import RPi.GPIO as gpio

#define the GPIO pins that we will use 
M1P1 = 5
M1P2 = 6
M2P1 = 13
M2P2 = 19
M3P1 = 26
M3P2 = 16
M4P1 = 20
M4P2 = 21

channel_list = [M1P1,M1P2,M2P1,M2P2,M3P1,M3P2,M4P1,M4P2]

def setup_gpio():
    try:
        gpio.setmode(gpio.BCM)
        mode = gpio.getmode()

        gpio.setchannel(channel_list, gpio.OUT, initial = gpio.LOW)
    except:
        print("** Unable to initialise gpio")


#define movement, if in automode, will move at default speed
#if in manual mode, speed depends on the controller intensity
def movement_auto(direction):
    if(direction == "up"):
        print("** Moving Forward")
        gpio.output(M1P1, gpio.HIGH)
        gpio.output(M1P1, gpio.HIGH)
        gpio.output(M1P1, gpio.HIGH)
        gpio.output(M1P1, gpio.HIGH)

def movement_controlled(direction, intensity):
    if(direction == "up"):
        print("** Moving Forward at intensity ", intensity)
        gpio.output(M1P1, gpio.HIGH)
        gpio.output(M1P1, gpio.HIGH)
        gpio.output(M1P1, gpio.HIGH)
        gpio.output(M1P1, gpio.HIGH)

def movement_stop():
    gpio(channel_list, gpio.LOW)