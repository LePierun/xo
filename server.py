import socket
import threading 

HEADER = 64
FORMAT = "utf-8"

DISCONNECTMSG = "!Dissconnect"

PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def HandleClient(conn, addr):
    print(f'[new conncetion] {addr} .')
    connected = True
    while connected:
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)

            if msg == DISCONNECTMSG:
                connected = False
    
    print(f"[{addr}] {msg}")
    conn.close()

def Start():
    server.listen()

    print(f"server on: {SERVER}")

    while True:
        conn , addr = server.accept()
        thread = threading.Thread(target=HandleClient, args=(conn, addr))
        thread.start()
print("[Startrd...]")
Start()
