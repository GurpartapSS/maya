import board
import busio
import adafruit_pca9685
import threading
import time

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

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

# Example: Move multiple servos simultaneously using threading
channels = [0, 1, 2, 3]  # List of channels to control
# duty_cycles = [4400, 5401, 4785, 5215]  # Define duty cycles for each channel
# duty_cycles = [4400, 2853, 3019, 4433]  # Define duty cycles for each channel
# duty_cycles = [4400, 4086, 5110, 3576]  # Define duty cycles for each channel
duty_cycles = [4400, 5572, 6568, 3604]  # Define duty cycles for each channel
# duty_cycles = [4400, 4956, 6141, 3414]  # Define duty cycles for each channel

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
