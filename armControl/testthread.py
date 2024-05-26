import board
import busio
import adafruit_pca9685
import threading
import time

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
m_pi = 3.14159265358979323846

# Initialize PCA9685
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 50  # Set PWM frequency to 50Hz

def move_servo(channel, duty_cycle):
    pca.channels[channel].duty_cycle = duty_cycle

def move_servo_thread(channel, duty_cycle):
    thread = threading.Thread(target=move_servo_smoothly, args=(channel, duty_cycle))
    thread.start()
    return thread

def move_servo_smoothly(channel, target_position, steps=50, delay=0.02):
    current_position = pca.channels[channel].duty_cycle
    increment = (target_position - current_position) / steps

    for _ in range(steps):
        current_position += increment
        pca.channels[channel].duty_cycle = int(current_position)
        time.sleep(delay)
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
# Example: Move multiple servos simultaneously using threading
channels = [0,7]  # List of channels to control
# duty_cycles = [4400, 5401, 4785, 5215]  # Define duty cycles for each channel
# duty_cycles = [4400, 2853, 3019, 4433]  # Define duty cycles for each channel
# duty_cycles = [4400, 4086, 5110, 3576]  # Define duty cycles for each channel
# duty_cycles = [4400, 5572, 6568, 3604]  # Define duty cycles for each channel
# duty_cycles = [4400, 4956, 6141, 3414]  # Define duty cycles for each channel
base_angle = 0
dc0 = ang2dutyCycle(1600, 7800, 4400,base_angle)
dc7 = ang2dutyCycle(1700, 7700, 4450, -(base_angle))
duty_cycles = [dc0, dc7]  # Define duty cycles for each channel

# Move each servo in a separate thread
threads = []
for channel, duty_cycle in zip(channels, duty_cycles):
    thread = move_servo_thread(channel, duty_cycle)
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Optional: Wait for some time to observe the servo movements
time.sleep(5)
