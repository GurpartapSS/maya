import socket
import time
import sys
sys.path.append('../')
import NetworkConstants as nc

class remoteclient:
    def __init__(self):
        self.__ADDR = (nc.SERVER, nc.PORT)
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connection(self):
        try:
            print(f"[Trying to connect to] {self.__ADDR}")
            self.__client.connect(self.__ADDR)
        except:
            print("U../botServer.py msg")
    def send(self,msg):
        message = msg.encode(nc.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(nc.FORMAT)
        send_length += b' ' * (nc.MSG_FORMAT - len(send_length))
        self.__client.send(send_length)
        self.__client.send(message)
    
    def disconnect(self):
        try:
            self.send(nc.DISCONNECT_MSG)
            self.__client.close()
        except:
            print(" **** Unable to disconnect check the network or try again ")