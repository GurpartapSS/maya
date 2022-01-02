# import socketio

# sio = socketio.Client()

# @sio.event
# def connect():
#     print('connection established')

# @sio.event
# def disconnect():
#     print('disconnected from server')

# sio.connect('http://10.0.0.203:5000', wait_timeout = 10)
# sio.wait()

import socket


MSG_FORMAT = 64 #fixing msg length
PORT = 5000
SERVER = '10.0.0.203'
FORMAT = 'utf-8'
DISCONNECT_MSG = "!Disconnect"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connection():
    try:
        print(f"[Trying to connect to] {ADDR}")
        client.connect(ADDR)
    except:
        print("Unable to connect")

def disconnect():
    try:
        send(DISCONNECT_MSG)
    except:
        print(" **** Unable to disconnect check the network or try again ")

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (MSG_FORMAT - len(send_length))
    client.send(send_length)
    client.send(message)

connection()
send("HEllo!") 
send(DISCONNECT_MSG)