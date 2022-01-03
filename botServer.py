
BUTTON_DISC     = 7
BUTTON_ACC      = BUTTON_DISC - 0
BUTTON_ROTR     = BUTTON_DISC - 1
BUTTON_REV      = BUTTON_DISC - 2
BUTTON_ROTL     = BUTTON_DISC - 3
BUTTON_LEFT     = BUTTON_DISC - 4
BUTTON_RIGHT    = BUTTON_DISC - 5



import socket
import threading
import actuatorControl


MSG_FORMAT = 64 #fixing msg length
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!Disconnect"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_clinet(conns, addr):
    print(f"[NEW connnection] {addr}")

    connected = True
    while(connected):
        # will not pass next line of code unless we recieve a msg
        msg_length = conns.recv(MSG_FORMAT).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conns.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            if msg == DISCONNECT_MSG:
                connected = False
            else:
                recv_data = int(msg) 
                recv_data = f'{recv_data:08b}'
                read_msg(recv_data)

    conns.close()

def start():
    server.listen()
    print(f" server listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        # creating a new thread with target function hadle and passing args
        thread = threading.Thread(target=handle_clinet, args=(conn, addr)) 
        thread.start()
        print(f"[Active connections] {threading.activeCount()-1}")

def read_msg(msg):
    print(f"** recv msg {int(msg)}")
    dir = "STOP"
    ## Check if any valid bit is set
    if (int(msg) & 127):
        acc = int((msg)[BUTTON_ACC])
        rev = int((msg)[BUTTON_REV])
        left = int((msg)[BUTTON_LEFT])
        right = int((msg)[BUTTON_RIGHT])
        rotate_left = int((msg)[BUTTON_ROTL])
        rotate_right = int((msg)[BUTTON_ROTR])
        if(acc):
            dir = "up"
        elif(rev):
            dir = "back"
        elif(left):
            dir = "left"
        elif(right):
            dir = "right"
        elif(rotate_left):
            dir = "rotate_left"
        elif(rotate_right):
            dir = "rotate_right"
    else:
        print("Stop!")
    
    actuatorControl.movement_auto(dir)

print(f" Starting Server .... ")
start()

