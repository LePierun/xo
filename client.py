import socket


HEADER = 64
FORMAT = "utf-8"

DISCONNECT_MSG = "!Dissconnect"

PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)