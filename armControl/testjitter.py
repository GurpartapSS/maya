import time
import board
import busio
from adafruit_pca9685 import PCA9685
import sys

m_pi = 3.14159265358979323846

def move_servo_smoothly(channel, target_position, steps=50, delay=0.02):
    current_position = pca.channels[channel].duty_cycle
    increment = (target_position - current_position) / steps

    for _ in range(steps):
        current_position += increment
        pca.channels[channel].duty_cycle = int(current_position)
        time.sleep(delay)

def move_servo_to_position(channel, position):
    pca.channels[channel].duty_cycle = int(position)

def ang2dutyCycle(back_dc, front_dc, mid_dc, angle):
    #angle will be 0 to 1.57 - we need to normalise it to 0 to 1.57
    something0to1 = abs(angle/(m_pi/2))
    if(angle > 0):
        delta = abs(front_dc - mid_dc) * something0to1
        dc = abs(mid_dc + delta) if (front_dc > back_dc) else abs(mid_dc - delta)
    else:
        delta = abs(mid_dc - back_dc) * something0to1
        dc = abs(mid_dc - delta) if (front_dc > back_dc) else abs(mid_dc + delta)
    return dc

def ang2dutyCycle2(rest_dc, front_dc, angle):
    #angle will be 0 to 1.57 - we need to normalise it to 0 to 1.57
    something0to1 = abs(angle/m_pi)
    delta = abs(front_dc - rest_dc) * something0to1
    dc = abs(rest_dc + delta)
    return dc

if __name__ == "__main__":
    # Initialize I2C bus and PCA9685
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50  # Set PWM frequency to 50Hz
    # Example usage: Move servo smoothly to a specific position

    if(sys.argv[1] == "m"):
        channel = int(sys.argv[2])
        target_position = int(sys.argv[3])
        print(f"moving {channel} to {target_position}")
        try:
            move_servo_smoothly(channel, target_position)
            time.sleep(1)  # Wait for 1 second

        except KeyboardInterrupt:
            pca.deinit()  # Cleanup PCA9685

    elif(sys.argv[1] == "c"):
        base_angle = float(sys.argv[2])
        a1_angle = float(sys.argv[3])
        a2_angle = float(sys.argv[4])
        wr_angle = float(sys.argv[5])
        cam_angle = float(sys.argv[6])
        dc = ang2dutyCycle(1600, 7800, 4400, base_angle)
        print(f"converting ch 0 {base_angle}: dc {int(dc)}")
        move_servo_smoothly(0,dc)
        dc = ang2dutyCycle(7800, 1800, 4800, a1_angle)
        print(f"converting ch 1 {a1_angle}: dc {int(dc)}")
        move_servo_smoothly(1,dc)
        dc = ang2dutyCycle2(1600, 7600, a2_angle)
        print(f"converting ch 2 {a2_angle}: dc {int(dc)}")
        move_servo_smoothly(2,dc)
        dc = ang2dutyCycle(7800, 1800, 4800, wr_angle)
        print(f"converting ch 3 {wr_angle}: dc {int(dc)}")
        move_servo_smoothly(3,dc)
        dc = ang2dutyCycle(7700, 1700, 4450, -base_angle)
        print(f"converting ch 7 {wr_angle}: dc {int(dc)}")
        move_servo_smoothly(4,dc)

    #0 base motor - 180 degrees - 1600(somewhat less han 90) to 7800(full 90 to left) mid_dc - 4400
    #1 arm1 motor - 180 degrees - 1800(somewhat less han 90) to 7800(full 90 back) mid_dc - 4800 negative value to increase from mid_dc
    #2 arm2 motor - 180 degrees - 1600(somewhat less han 90) to 7600(full 90 forward) mid_dc - 4600 negative value to decrease from mid_dc
    #3 wrist motor - 180 degrees - 1800(somewhat less han 90) to 7800(full 90 forward) mid_dc - 4800 negative value to decrease from mid_dc
    #4 arm camera motor - 180 degrees - 1700(90)clockwise to 7700(full 90 forward) mid_dc - 4450 negative value to decrease from mid_dc
