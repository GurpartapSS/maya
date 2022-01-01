# import eventlet
# import socketio

# sio = socketio.Server()
# app = socketio.WSGIApp(sio)

# @sio.event
# def connect(sid, environ):
#     print('connect ', sid)

# @sio.event
# def my_message(sid, data):
#     print('message ', data)

# @sio.event
# def disconnect(sid):
#     print('disconnect ', sid)

# if __name__ == '__main__':
#     eventlet.wsgi.server(eventlet.listen(('10.0.0.203', 5000)), app)


import socket
import threading


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



print(f" Starting Server .... ")
start()

