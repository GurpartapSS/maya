import time

class pidController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0
        self.last_time = time.time()

    def calculate(self, setpoint, pv):
        # Get current time
        now = time.time()
        dt = now - self.last_time

        # Calculate error
        error = setpoint - pv

        # Proportional term
        Pout = self.kp * error
        if(self.ki or self.kd):
            # Integral term
            self.integral += error * dt
            Iout = self.ki * self.integral

            # Derivative term
            derivative = (error - self.prev_error) / dt
            Dout = self.kd * derivative

        # Calculate total output
        # output = Pout + Iout + Dout
        output = Pout

        # Save error and time for the next iteration
        self.prev_error = error
        self.last_time = now

        return output

if __name__ == "__main__":

    kp = 1.0
    ki = 0.1
    kd = 0.05

    # Create PID controller
    pid = PID(kp, ki, kd)

    # Setpoint and initial process variable
    setpoint = 100.0
    pv = 0.0

    # Simulate a process for 100 steps
    for i in range(100):
        # Calculate the control variable
        control = pid.calculate(setpoint, pv)

        # Simulate the process response (here we simply add the control output to pv)
        pv += control

        # Print current process variable
        print(f"Step {i} - PV: {pv}")

        # Sleep for a short duration (e.g., 100 ms)
        time.sleep(0.1)
