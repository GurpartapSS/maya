import busio
from adafruit_pca9685 import PCA9685
import time
from collections import deque

numberofparts = 4

# base motor - 2500 to 8000 mid - 6000
# base motor - 2500 to 8000 mid - 5500
# base motor - 1500 to 7000 mid - 3500

class arm:

    def __init__(self):
        # SG90 servo motor specifications
        self.mask_direction = 3 #b'11'
        self.mask_resolution = 0x300 #b'11'
        self.base_motor = 0
        self.shoulder_motor = 1
        self.arm_motor = 2
        self.wrist_motor = 3

        self.pulse_width_min = 1800  # Minimum pulse width in microseconds
        self.pulse_width_max = 7800  # Maximum pulse width in microseconds
        self.pulse_width_center = 4800  # understood right?!
        self.dcCache = {self.wrist_motor:self.pulse_width_center, self.shoulder_motor:6000,
                            self.base_motor:self.pulse_width_center, self.arm_motor:6000}
        self.min_step_Size = 100
        self.motion_step = 100
        self.partName = deque()
        self.partMotion = deque()
        self.resolution = 1

        # Create the I2C bus interface.
        i2c_bus = busio.I2C(3, 2)   #Board SCL and SDA

        # Create a PCA9685 instance.
        self.pca = PCA9685(i2c_bus)
        self.pca.frequency = 50  # Set PWM frequency to 50 Hz for SG90 servo motor

        self.moveToCenter()

    def move_servo_smoothly(self, channel, target_position, steps=50, delay=0.02):
        current_position = self.pca.channels[channel].duty_cycle
        increment = (target_position - self.current_position) / steps

        for _ in range(steps):
            current_position += increment
            self.pca.channels[channel].duty_cycle = int(current_position)
            time.sleep(delay)

    def movePartByDC(self):
        while(len(self.partName) != 0):
            part = self.partName.popleft()
            motion = 1 if self.partMotion.popleft() == 1 else -1
            if(part in self.dcCache):
                cacheDC = (motion * self.motion_step) + self.dcCache[part]
                dc_new = cacheDC if (self.pulse_width_min < cacheDC < self.pulse_width_max) else self.dcCache[part]
                self.dcCache[part] = dc_new
                print(f"moving part {part} to DC {dc_new}")
                self.pca.channels[part].duty_cycle = dc_new
                time.sleep(.2)
    
    def movePartByAngle(self, part, angle):
        self.pca.channels[part].duty_cycle = angle

    def moveToCenter(self):
        self.pca.channels[self.base_motor].duty_cycle = self.pulse_width_center
        time.sleep(.3)
        self.pca.channels[self.wrist_motor].duty_cycle = self.pulse_width_center
        time.sleep(.3)
        self.pca.channels[self.shoulder_motor].duty_cycle = 6000
        time.sleep(.3)
        self.pca.channels[self.arm_motor].duty_cycle = 6000
    
    def __delete__(self):
        self.pca.deinit()  # Clean up PCA9685


    def decode(self, message):
        # should return the value for each joint 
        # message is 16 bit integer
        # lower 8 bit is positive movement and upper 8 bit is negative movement
        print(f"received {message}")
        count = 0 
        while(message & 0x3ff):
            if(message & 0x300):
                self.resolution = min(max(self.resolution + (1 if message & 0x100 else -1),1),10)
                self.motion_step = self.min_step_Size * self.resolution
                print(f"new resolution {self.resolution}")
            s = message & self.mask_direction
            if (s):
                self.partName.append(count)
                self.partMotion.append(1 if s%2 == 0 else 0)
            count = count + 1
            message = message >> 2
        print(self.partMotion, self.partName)
        self.movePartByDC()
      

if __name__ == "__main__":
    try:
        message = 15
        a1 = arm()
        a1.decode(message)
        a1.decode(message)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        pass

    finally:
        # Reset servo motor to 90 degrees and cleanup
        # a1.moveToCenter()  # Set all servo angle to 90 degrees
        time.sleep(.2)  # Wait for the servo to reach the center position
