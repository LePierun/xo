import socket
import pygame as pg
from enum import Enum
import threading
from serverConstant import PORT, FORMAT, HEADER
import serverConstant as sc

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



class GameState(Enum):
    MyTurn = 1
    FoeTurn = 2



def Send(msg):
    msg = str(msg)
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)

def Recive():
    msgLength = client.recv(HEADER).decode(FORMAT)
    if msgLength:
        msgLength = int(msgLength)
        msg = client.recv(msgLength).decode(FORMAT)
        return(msg)

connectionid = Recive()
print(f'this is ur id: {connectionid}')

pg.init()
screensize = (1280, 720)
screen = pg.display.set_mode(screensize)
CENTER = (screensize[0]/2,screensize[1]/2)
clock = pg.time.Clock()
running = True
#--------------------------------------------------------Start
gState = GameState.MyTurn 
boardSize = 10
potetoes = []
potetoesCol = [] 
potSize = 10
miceCol = pg.Rect(0,0,10,10) 

class Poteto():
    x = None
    y = None
    position = ()
    fill = False

    def __init__(self, x,y, position) -> None:
        self.x = x
        self.y = y
        self.position = position
        self.fill = False

    def Fill(self):
        fill = True

def GenerateBoard(br):
    for i in range(br):
        for j in range(i):
            spacebetwen = potSize*2
            temPos = (CENTER[0]+ spacebetwen * j - i* spacebetwen/2, CENTER[1] + spacebetwen * i )
            potetoes.append(Poteto(j, i , temPos))
            potetoesCol.append(pg.Rect(temPos[0]-potSize,temPos[1]-potSize, spacebetwen,spacebetwen))

def Graphic():
    for i in range(potetoes.__len__()):
        if potetoes[i].fill == True:
            pg.draw.circle(screen, "white",potetoesCol[i].center, potSize, 0)
        else:
            pg.draw.circle(screen, "white",potetoesCol[i].center, potSize, 2)
    pg.display.flip()

def FillPoteto(indx):
    potetoes[indx].Fill()

def Turn():
    pass

def OffTime():
    pass
    
selectedPot = -1

#----generate board -------------------------------------------------------------------------------
GenerateBoard(boardSize)

while running:
    if gState == GameState.MyTurn:
        selectedPot = miceCol.collidelist(potetoesCol)

    elif gState == GameState.FoeTurn:
        msg = Recive()

        if msg == sc.FILLED:
            filedPoteto = Recive()
            FillPoteto(filedPoteto)
            print(msg)

        if msg == sc.YOURTURN:
            msg = Recive()
            print(msg)
            gState = GameState.MyTurn

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONUP:
            if selectedPot != -1 and gState == GameState.MyTurn:
                Send(sc.FILLED)
                Send(selectedPot)
                potetoes[selectedPot].fill = True
                gState = GameState.FoeTurn

    screen.fill("black")
    micepos = pg.mouse.get_pos()
    miceCol = pg.Rect(micepos,(1,1)) 








    Graphic()
    clock.tick(60) 

pg.quit()


