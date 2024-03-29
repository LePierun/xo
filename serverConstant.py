HEADER = 64
FORMAT = "utf-8"
PORT = 8000


DISCONNECT_MSG = "!Dissconnect"
FILLED = "filed"
ENDTURN = "endturn"
YOURTURN = "yourturn"

def Fillinfo(connid, slot):
    return f'{FILLED}:{slot}:{connid}'