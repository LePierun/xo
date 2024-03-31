import socket
import pygame as pg
from enum import Enum
import threading
from serverConstant import PORT, FORMAT, HEADER
import serverConstant as sc

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = ("192.168.1.9", PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


enemyscore = 0
myscore = 0
playercolor = "green"
enemycolor = "red"
# curplayercolor = playercolor

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

pg.font.init()
pg.init()
screensize = (1280, 720)
screen = pg.display.set_mode(screensize)
CENTER = (screensize[0]/2,screensize[1]/2)
clock = pg.time.Clock()
running = True
#--------------------------------------------------------Start
gState = GameState.FoeTurn 
boardSize = 10
potetoes = []
potetoesCol = []
scoringLines = [] 
scoringCros = []
a = 0
for i in range(boardSize): a += i
maxPolas = a

maxPolas -= 1
potSize = 10
miceCol = pg.Rect(0,0,10,10) 

class Poteto():
    neig1 = None
    neig2 = None
    neig3 = None
    neig4 = None
    neig5 = None
    neig6 = None
    idikmany = -1
    firstInRow = -1
    lastInRow = -1
    row = -1
    owned = False
        #  1 2
        # 6 o 3
        #  5 4  

    x = None
    y = None
    position = ()
    fill = False

    def __init__(self, x,y, position,id) -> None:
        self.x = x
        self.y = y
        self.position = position
        self.fill = False
        self.idikmany = id

        self.row = self.GetRow()
        self.firstInRow = self.GetFirstInRow(self.row)
        self.lastInRow = self.firstInRow + self.row


        if id != self.firstInRow: 
            if (id - 1) >= self.firstInRow:
                self.neig6 = id - 1
            if (id - self.row -1) >= 0:
                self.neig1 = id - self.row -1

        if id != self.lastInRow:
            if (id + 1) <= self.lastInRow:
                self.neig3 = id + 1
            if (id - self.row) >= 0:
                self.neig2 = id - self.row


        if (id + self.row + 2) <= maxPolas:
            self.neig4 = id + self.row + 2
        if (id + self.row + 1) <= maxPolas:
            self.neig5 = id + self.row + 1

    def IsRowFilled(self):
        a = []
        for i in range(self.firstInRow,self.lastInRow+1):
            a.append(i)

        return a
        
    
    def Is4Filled(self):
        temp = ''
        temp = f":{self.idikmany}:"

        if self.neig4 != None:
            n = potetoes[self.neig4]
            temp += str(n.Is4Filled())
        # elif self.idikmany == maxPolas+1:
        #     ret
        return temp


    
    def Is1Filled(self):
        temp = ''
        temp = f":{self.idikmany}:"

        if self.neig1 != None:
            n = potetoes[self.neig1]
            temp += str(n.Is1Filled())

        return temp
    
    def Is14Filled(self):
        a = self.Is1Filled()
        b = self.Is4Filled()
        a = a.replace("::","|")
        a = a.replace(":","")
        a = a.split('|')
        b = b.replace("::","|")
        b = b.replace(":","")
        b = b.split('|')
        c = a[::-1] + b
        return c
    
    def Is25Filled(self):
        a = self.Is2Filled()
        b = self.Is5Filled()
        a = a.replace("::","|")
        a = a.replace(":","")
        a = a.split('|')
        b = b.replace("::","|")
        b = b.replace(":","")
        b = b.split('|')
        c = a[::-1] + b
        return c
    
    def Is2Filled(self):
        temp = ''
        temp = f":{self.idikmany}:"

        if self.neig2 != None:
            n = potetoes[self.neig2]
            temp += str(n.Is2Filled())

        return temp
    
    def Is5Filled(self):
        temp = ''
        temp = f":{self.idikmany}:"

        if self.neig5 != None:
            n = potetoes[self.neig5]
            temp += str(n.Is5Filled())

        return temp

    def getAllNeighbor(self):
        ar = [self.neig1, self.neig2, self.neig3, self.neig4, self.neig5,self.neig6]
        return ar

    def GetRow(self):
        smtn = self.idikmany
        temp = 0
        step = 0

        for i in range(2,boardSize+1):
            if temp >= smtn:
                return step
            step += 1 
            temp += i
        return -69
    
    def GetFirstInRow(self, param):
        temp = 0
        for i in range(param+1):
            temp += i
        return temp
    def Fill(self):
        self.fill = True

def GenerateBoard(br):
    for i in range(br):
        for j in range(i):
            spacebetwen = potSize*2
            temPos = (CENTER[0]+ spacebetwen * j - i* spacebetwen/2, CENTER[1] + spacebetwen * i )
            potetoes.append(Poteto(j, i , temPos,potetoes.__len__()))
            potetoesCol.append(pg.Rect(temPos[0]-potSize,temPos[1]-potSize, spacebetwen,spacebetwen))

def Graphic():
    for i in range(potetoes.__len__()):
        pot = potetoes[i]
        if pot.fill == True:
            if pot.owned == True:
                pg.draw.circle(screen, playercolor,potetoesCol[i].center, potSize, 0)
            else:
                pg.draw.circle(screen, enemycolor,potetoesCol[i].center, potSize, 0)

        else:
            pg.draw.circle(screen, "grey",potetoesCol[i].center, potSize, 2)
    
    for i in scoringLines:
        pg.draw.line(screen, playercolor, potetoesCol[i[0]].center,potetoesCol[i[1]].center,5)

    for i in scoringCros:
        pg.draw.line(screen, enemycolor, potetoesCol[int(i[0])].center,potetoesCol[int(i[1])].center,5)
    pg.display.flip()

def FillMyPoteto(indx):
    a = potetoes[int(indx)]
    a.Fill()
    a.owned = True

def FillPoteto(indx):
    a = potetoes[int(indx)]
    a.Fill()

selectedPot = -1

#----generate board -------------------------------------------------------------------------------
GenerateBoard(boardSize)

# for i in range(maxPolas):
#     print(potetoes[i].Is25Filled())
# print(potetoes[8].IsRowFilled())
# print(potetoes[35].Is25Filled())
# print(potetoes[35].Is14Filled())



def IsLineFill(arr):
        for i  in arr:
            i = int(i)
            if potetoes[i].fill == False:
                return False
        return True

def AddPoints(scor):
    Send(sc.SCORING)
    Send(scor)
    Send(scoringLines[scoringLines.__len__()-1][0])
    Send(scoringLines[scoringLines.__len__()-1][1])
    global myscore
    myscore += scor

def IfLineFilled(arr):
    if IsLineFill(arr):
        a = (int(arr[0]),int(arr[arr.__len__()-1]))
        scoringLines.append(a)

        AddPoints(arr.__len__())

def AddEnemyScore(scr):
    global enemyscore
    enemyscore += int(scr)

my_font = pg.font.SysFont('Comic Sans MS', 42)
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            

        if event.type == pg.MOUSEBUTTONUP:
            if selectedPot != -1 and gState == GameState.MyTurn:
                z = potetoes[int(selectedPot)]
                if z.fill == False:
                    gState = GameState.FoeTurn
                    FillMyPoteto(selectedPot)
                    IfLineFilled(z.IsRowFilled())
                    IfLineFilled(z.Is25Filled())
                    IfLineFilled(z.Is14Filled())
                    
                    Send(sc.FILLED)
                    Send(selectedPot)
                    Send(sc.NEXT)



    
    screen.fill("black")
    enemyscoretxt = my_font.render(str(enemyscore), False, "red")
    myscoretxt = my_font.render(str(myscore), False, "green")


    screen.blit(enemyscoretxt, (200,200))
    screen.blit(myscoretxt, (500,200))



    micepos = pg.mouse.get_pos()


    smtn = pg.Rect(1,1 ,50, 50)
    if gState == GameState.FoeTurn:
        pg.draw.rect(screen, "red", smtn)
    else:
        pg.draw.rect(screen, "green", smtn)

    Graphic()


    if gState == GameState.MyTurn:
        miceCol = pg.Rect(micepos,(1,1)) 
        selectedPot = miceCol.collidelist(potetoesCol)
        

    elif gState == GameState.FoeTurn:
        MSG = Recive()
        selectedPot = -1

        if MSG == sc.YOURTURN:
            gState = GameState.MyTurn
            
            Send(sc.GETLASTCHANG)
            lastch = Recive()
            AddEnemyScore(Recive())

            point = (Recive(),Recive())
            scoringCros.append(point)
            # Send(sc.GETLASTCHANG)

            if lastch != sc.NOTHING:
                FillPoteto(lastch)

    clock.tick(60) 

Send(sc.DISCONNECT_MSG)
pg.quit()


