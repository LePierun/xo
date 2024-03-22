import socket
import pygame as pg
from enum import Enum


HEADER = 64
FORMAT = "utf-8"

DISCONNECT_MSG = "!Dissconnect"

PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

print(client)

class Color(Enum):
    Game = 1
    MainMane = 2



def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)



pg.init()
screen = pg.display.set_mode((1280, 720))
CENTER = (1280/2,720/2)
clock = pg.time.Clock()
running = True
#--------------------------------------------------------Start
potetoes = []

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



while running:
    micepos = pg.mouse.get_pos()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("black")
    
    for i in range(10):
        rows = []
        for j in range(i):
            spacebetwen = 24
            temPos = (CENTER[0]+ spacebetwen * j - i* spacebetwen/2, CENTER[1] + spacebetwen * i )
            rows.append(Poteto(temPos[0],temPos[1],temPos))
            pg.draw.circle(screen, "white",temPos, 10, 2)
        potetoes.append(rows)

    print(potetoes)

    pg.display.flip()

    clock.tick(60) 

pg.quit()
