import socket
import threading 
import serverConstant as sc
from serverConstant import HEADER, FORMAT, DISCONNECT_MSG, PORT


SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



def Send(msg,conn):
    msg = str(msg)
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    conn.send(send_len)
    conn.send(message)

def Recive(conn):
    msgLength = conn.recv(HEADER).decode(FORMAT)
    if msgLength:
        msgLength = int(msgLength)
        msg = conn.recv(msgLength).decode(FORMAT)
        return(msg)

def SendOther(msg, id):
    for i in connections:
        if i != id:
            Send(msg,i.conn)

class Connection():
    activ = False
    conn = None
    def __init__(self,conn) -> None:
        self.conn = conn


firstPlayer = True
lastChang = -1
def HandleClient(conn, addr):
    global lastChang
    print(f'[new conncetion] {addr} .')
    connected = True
    msg = " none "
    connections.append(Connection(conn))
    conid = connections.__len__()-1
    Send(conid,conn)

    global firstPlayer
    if firstPlayer:
        Send(sc.YOURTURN,conn)
        firstPlayer = False

    while connected:
        msg = Recive(conn)

        if msg == DISCONNECT_MSG:
            connected = False

        elif msg == sc.GETLASTCHANG:
            Send(lastChang,conn)

        elif msg == sc.NEXT:
            NextTurn()
            Send(sc.YOURTURN,connections[activCon].conn)

        elif msg == sc.FILLED:
            whitchpoteto = Recive(conn)
            lastChang = whitchpoteto
            
            # Send(sc.YOURTURN,connections[activCon].conn)

        else:
            print(f"[{addr}] {msg}")
                
    
    conn.close()

connections = []
lastMsg = {} 



activCon = 0
def NextTurn():
    global activCon
    activCon += 1
    if activCon > connections.__len__()-1:
        activCon = 0


def Start():
    server.listen()

    print(f"server on: {SERVER}")

    while True:
        conn , addr = server.accept()
        thread = threading.Thread(target=HandleClient, args=(conn, addr))
        thread.start()


print("[Startrd...]")
Start()
