import socket
import time

BUTTON_ACC      = 0
BUTTON_ROTR     = 1
BUTTON_REV      = 2
BUTTON_ROTL     = 3
BUTTON_LEFT     = 4
BUTTON_RIGHT    = 5
BUTTON_DISC     = 7

MSG_FORMAT = 64 #fixing msg length
PORT = 5000
SERVER = '10.0.0.203'
FORMAT = 'utf-8'
DISCONNECT_MSG = "!Disconnect"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def Reconnect():  #Ive created a new function called Reconnect, because, .., well it works fine for now
    try:
        global s #Its accessing the global socket variable
        client = ""   #blanks it out (not sure if i have to blank it out)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create again a new socket
        client.connect((ADDR)) # It tries to connect again
    except:
        time.sleep(1)
        print("Reconnecting")
        Reconnect()

def connection():
    try:
        print(f"[Trying to connect to] {ADDR}")
        client.connect(ADDR)
    except:
        print("Unable to connect")
        Reconnect()

def disconnect():
    try:
        send(DISCONNECT_MSG)
        client.close()
    except:
        print(" **** Unable to disconnect check the network or try again ")

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (MSG_FORMAT - len(send_length))
    client.send(send_length)
    client.send(message)


## Test connection: 

# connection()
# send(str(1))
# send(DISCONNECT_MSG)