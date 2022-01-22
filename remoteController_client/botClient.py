import socket
import time
import sys
sys.path.append('../')
import constants

class remoteclient:
    def __init__(self):
        self.__nc = constants.networkConstant()
        self.__ADDR = (self.__nc.SERVER, self.__nc.PORT)
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connection(self):
        try:
            print(f"[Trying to connect to] {self.__ADDR}")
            self.__client.connect(self.__ADDR)
        except:
            print("U../botServer.py msg")
    def send(self,msg):
        message = msg.encode(self.__nc.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.__nc.FORMAT)
        send_length += b' ' * (self.__nc.MSG_FORMAT - len(send_length))
        self.__client.send(send_length)
        self.__client.send(message)
    
    def disconnection(self):
        try:
            self.send(self.__nc.DISCONNECT_MSG)
            self.__client.close()
        except:
            print(" **** Unable to disconnect check the network or try again ")