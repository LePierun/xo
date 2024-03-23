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
    



def HandleClient(conn, addr):
    print(f'[new conncetion] {addr} .')
    connected = True
    msg = " none "
    connections.append(Connection(conn))
    conid = connections.__len__()-1
    Send(conid,conn)
    while connected:
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            lastMsg[f'{conn}:{addr}'] = msg
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)
            

            if msg == DISCONNECT_MSG:
                connected = False
            if msg == sc.FILLED:
                whitchpoteto = Recive(conn)
                SendOther(whitchpoteto, conid)
                NextTurn()
                Send(sc.YOURTURN,connections[activCon].conn)
                pass
            else:

                print(f"[{addr}] {msg}")
                
    
    conn.close()

connections = []
lastMsg = {} 



activCon = 0
def NextTurn():
    global activCon
    activCon += 1
    if activCon > connections.__len__():
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
