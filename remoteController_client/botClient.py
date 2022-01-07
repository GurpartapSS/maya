import socket
import time
import NetworkConstants as nc

ADDR = (nc.SERVER, nc.PORT)

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
        send(nc.DISCONNECT_MSG)
        client.close()
    except:
        print(" **** Unable to disconnect check the network or try again ")

def send(msg):
    message = msg.encode(nc.FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(nc.FORMAT)
    send_length += b' ' * (nc.MSG_FORMAT - len(send_length))
    client.send(send_length)
    client.send(message)


## Test connection: 

# connection()
# send(str(1))
# send(DISCONNECT_MSG)