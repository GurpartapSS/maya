import os
import sys

# Get the parent directory of the current file (child_module.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the sys.path
sys.path.append(parent_dir)


import socket
import threading
from actuatorControl import actuator
from constants import networkConstant, joystickConstant
import armControl.armDriver as armDriver

nc = networkConstant()
jc = joystickConstant()
ac = actuator()
arm = armDriver.arm()

class rcServer:
    def __init__(self):
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, nc.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

    def handle_clinet(self, conns, addr):
        print(f"[NEW connnection] {addr}")

        connected = True
        while(connected):
            # will not pass next line of code unless we recieve a msg
            msg_length = conns.recv(nc.MSG_FORMAT).decode(nc.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conns.recv(msg_length).decode(nc.FORMAT)
                # print(f"[{addr}] {msg}")
                if msg == nc.DISCONNECT_MSG:
                    connected = False
                else:
                    recv_data = int(msg) 
                    # recv_data = f'{recv_data:16b}'
                    arm.decode(recv_data)
                    # read_msg(recv_data)

        conns.close()

    def start(self):
        self.server.listen()
        print(f" server listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            # creating a new thread with target function hadle and passing args
            self.thread = threading.Thread(target=self.handle_clinet, args=(conn, addr)) 
            self.thread.start()
            print(f"[Active connections] {threading.activeCount()-1}")

    def __del__(self):
        self.thread.join()
        self.server.close()


if __name__ == "__main__":
    # print(f" Starting Server .... ")
    # motor = actuatorControl.actuator()
    # motor.setup_gpio()
    try:
        s = rcServer()
        s.start()

    except KeyboardInterrupt:
        print("KeyboardInterrupt Exiting izzat se")

    finally:
        print("Fin!!")