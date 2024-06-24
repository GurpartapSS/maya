#!/home/ubuntu/autoBot/env_bot/bin/python

import time
import board
import busio
from adafruit_pca9685 import PCA9685
import sys

import threading
import time
from collections import deque
import random

m_pi = 3.14159265358979323846


class armDriver:
    def __init__(self):
        # Initialize I2C bus and PCA9685
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c)
        self.pca.frequency = 50  # Set PWM frequency to 50Hz
        # self.barrier = threading.Barrier(6)
        self.moving = 0
        self.q = deque()
         
        self.jointNameMap = {'bases_joint':0,'base_arm1_joint':1,'arm1_arm2_joint':2,
                            'arm2_arm3_joint':3,'wrist_gripl_joint':13, 'arm3_camera_joint':15}
    def isMoving(self):
       return self.moving

    def set_jointStates(self, target_positions, names, steps=50, delay=0.02):
        threads = []
        print(names)
        for i, name in enumerate(names):
            if(name in self.jointNameMap):
                thread = self.move_servo_thread(self.jointNameMap[name], target_positions[i])
                threads.append(thread)
        # self.barrier.wait()
        for thread in threads:
            thread.join()  # Wait for all threads to finish
        self.moving = 0

    def move_servo_thread(self, channel, angle):
        if(channel == 0):
            dc = int(self.ang2dutyCycle(1600, 7800, 4400, angle))
            print(f"converting ch 0 {angle}: dc {int(dc)}")
        elif(channel == 1):
            # dc = int(self.ang2dutyCycle(7800, 1700, 4850, angle))
            dc = int(self.ang2dutyCycle(5500, 1100, 3400, angle))
            print(f"converting ch 1 {angle}: dc {int(dc)}")
        elif(channel == 2):
            # dc = self.ang2dutyCycle2(1600, 7600, angle)
            dc = int(self.ang2dutyCycle2_newmotor(3400, angle))
            print(f"converting ch 2 {angle}: dc {int(dc)}")
        elif(channel == 3):
            # dc = int(self.ang2dutyCycle(7500, 1600, 4300, angle))
            dc = int(self.ang2dutyCycle(7700, 1600, 4500, angle))
            print(f"converting ch 3 {angle}: dc {int(dc)}")
        elif(channel == 13):
            dc = self.gripperCycles(1600, 3600, angle)
            print(f"converting ch 14 {angle}: dc {int(dc)}")
        elif(channel == 15):
            dc = int(self.ang2dutyCycle(1700, 7700, 4450, angle))
            print(f"converting ch 15 {angle}: dc {int(dc)}")
        thread = threading.Thread(target=self.move_servo_smoothly, args=(channel, dc))
        thread.start()
        return thread
    
    def move_servo_smoothly(self, channel, target_position, min_steps=10, max_steps=50, delay=0.02):
        print(f"Inner Moving {channel} : {target_position}")
        current_position = self.pca.channels[channel].duty_cycle
        difference = abs(target_position - current_position)
    
        # Scale the steps based on the difference with a maximum difference of 8000
        if difference > 300:
            difference = 3000  # Cap the difference at 8000

        steps = int(min_steps + (difference / 3000) * (max_steps - min_steps))
        steps = max(min(steps, max_steps), min_steps)
        
        increment = (target_position - current_position) / steps

        for _ in range(steps):
            current_position += increment
            self.pca.channels[channel].duty_cycle = int(current_position)
            time.sleep(delay)

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
    
    def ang2dutyCycle2_newmotor(self, rest_dc, angle):
        # step_angle * angle + rest_dc
        return int(rest_dc + (angle * (2100/m_pi) * 2 ))

    def gripperCycles(self, open_dc, close_dc, angle):
        return(close_dc - (open_dc)*(angle))
# base motor - 180 degrees - 1600(somewhat less han 90) to 7800(full 90 to left) mid_dc - 4400
    # arm1 motor - 180 degrees - 1800(somewhat less han 90) to 7800(full 90 back) mid_dc - 4800 negative value to increase from mid_dc
    # arm1 motor 2 - 90 forward - 1100 mid - 3400 90 back 5500
    # arm2 motor - 180 degrees - 1600(somewhat less han 90) to 7600(full 90 forward) mid_dc - 4500 negative value to decrease from mid_dc
    # arm2 motor 2 - -90 1300 0 3500 
    # wrist motor - 180 degrees - 1600(somewhat less han 90) to 7500(full 90 forward) mid_dc - 4300 negative value to decrease from mid_dc
    # wrist motor 2 - 90 forward 1900 - mid - 3400 90 back 5500
if __name__ == "__main__":
    ad = armDriver()
    jointnames = ['bases_joint','base_arm1_joint','arm1_arm2_joint',
                                'arm2_arm3_joint','arm3_camera_joint','wrist_gripl_joint'] 
    positions = [0.0, 0.0, 1.57, 0, 0 ,0]
    s = 0
    while(s<1):
        q = []
        print(ad.isMoving())
        for i,p in enumerate(positions):
            if(i == 5):
                q.append(1)
            else:            
                random_number = random.uniform(-1, 1)
                random_number/10
                q.append(p+round(random_number,2))
        ad.set_jointStates(q,jointnames)
        print(ad.isMoving())
        time.sleep(1)
        s+=0.2