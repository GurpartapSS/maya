#!/home/ubuntu/autoBot/env_bot/bin/python

import time
import board
import busio
from adafruit_pca9685 import PCA9685
import sys

import threading
import time
from collections import deque


m_pi = 3.14159265358979323846


class armDriver:
    def __init__(self):
        # Initialize I2C bus and PCA9685
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c)
        self.pca.frequency = 50  # Set PWM frequency to 50Hz
        self.barrier = threading.Barrier(4)
        self.moving = 0
        self.q = deque()
    def isMoving(self):
       return self.moving

    def set_jointStates(self, rad, target_positions, steps=50, delay=0.02):
        self.moving = 1
        threads = []
        for i, target_position in enumerate(target_positions):
            if(rad == 1):
                thread = self.move_servo_thread_rad(i, target_position)
            else:
                thread = self.move_servo_thread(i, target_position)
            threads.append(thread)
        self.barrier.wait()
        self.moving = 0

    def move_servo_thread(self, channel, angle):
        if(channel == 0):
            dc = self.ang2dutyCycle(7800, 1800, 4800, angle)
            print(f"converting ch 0 {angle}: dc {int(dc)}")
        elif(channel == 1):
            dc = self.ang2dutyCycle2(1600, 7600, angle)
            print(f"converting ch 1 {angle}: dc {int(dc)}")
        elif(channel == 2):
            dc = self.ang2dutyCycle(1600, 7800, 4400, angle)
            print(f"converting ch 2 {angle}: dc {int(dc)}")
        elif(channel == 3):
            dc = self.ang2dutyCycle(7800, 1800, 4800, angle)
            print(f"converting ch 3 {angle}: dc {int(dc)}")
        elif(channel == 4):
            dc = self.ang2dutyCycle(7700, 1700, 4450, angle)
            print(f"converting ch 7 {angle}: dc {int(dc)}")
        thread = threading.Thread(target=self.move_servo_smoothly, args=(channel, dc))
        thread.start()
        return thread
    
    def move_servo_thread_rad(self, channel, angle):
        if(channel == 0):
            dc = self.ang2dutyCycle(1600, 7800, 4400, angle)
            print(f"converting ch 0 {angle}: dc {int(dc)}")
        elif(channel == 1):
            dc = self.ang2dutyCycle(7800, 1800, 4800, angle)
            print(f"converting ch 1 {angle}: dc {int(dc)}")
        elif(channel == 2):
            dc = self.ang2dutyCycle2(1600, 7600, angle)
            print(f"converting ch 2 {angle}: dc {int(dc)}")
        elif(channel == 3):
            dc = self.ang2dutyCycle(7800, 1800, 4800, angle)
            print(f"converting ch 3 {angle}: dc {int(dc)}")
        elif(channel == 4):
            dc = self.ang2dutyCycle(1700, 7700, 4450, angle)
            print(f"converting ch 7 {angle}: dc {int(dc)}")
        thread = threading.Thread(target=self.move_servo_smoothly, args=(channel, dc))
        thread.start()
        return thread
    
    def move_servo_smoothly(self, channel, target_position, steps=50, delay=0.02):
        print(f"Inner Moving {channel} : {target_position}")
        current_position = self.pca.channels[channel].duty_cycle
        increment = (target_position - current_position) / steps

        for _ in range(steps):
            current_position += increment
            self.pca.channels[channel].duty_cycle = int(current_position)
            time.sleep(delay)
        self.barrier.wait()

    def ang2dutyCycle(self, back_dc, front_dc, mid_dc, angle):
    #angle will be 0 to 1.57 - we need to normalise it to 0 to 1.57
        something0to1 = abs(angle/(m_pi/2))
        if(angle > 0):
            delta = abs(front_dc - mid_dc) * something0to1
            dc = abs(mid_dc + delta) if (front_dc > back_dc) else abs(mid_dc - delta)
        else:
            delta = abs(mid_dc - back_dc) * something0to1
            dc = abs(mid_dc - delta) if (front_dc > back_dc) else abs(mid_dc + delta)
        return dc

    def ang2dutyCycle2(self, rest_dc, front_dc, angle):
        #angle will be 0 to 1.57 - we need to normalise it to 0 to 1.57
        something0to1 = abs(angle/m_pi)
        delta = abs(front_dc - rest_dc) * something0to1
        dc = abs(rest_dc + delta)
        return dc


# base motor - 180 degrees - 1600(somewhat less han 90) to 7800(full 90 to left) mid_dc - 4400
    # arm1 motor - 180 degrees - 1800(somewhat less han 90) to 7800(full 90 back) mid_dc - 4800 negative value to increase from mid_dc
    # arm2 motor - 180 degrees - 1600(somewhat less han 90) to 7600(full 90 forward) mid_dc - 4600 negative value to decrease from mid_dc
    # wrist motor - 180 degrees - 1800(somewhat less han 90) to 7800(full 90 forward) mid_dc - 4800 negative value to decrease from mid_dc