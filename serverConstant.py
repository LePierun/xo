HEADER = 64
FORMAT = "utf-8"
PORT = 8000


DISCONNECT_MSG = "!Dissconnect"
FILLED = "filed"
ENDTURN = "endturn"
YOURTURN = "yourturn"
GETLASTCHANG = "getlastchang"
NEXT = "next"
NOTHING ="-1"
def Fillinfo(connid, slot):
    return f'{FILLED}:{slot}:{connid}'