import socket
import sys
import threading
import time
from typing import runtime_checkable
import misc

#server related variables
server=("http://ludicroustech.ca", 55555)

#state related variables, these describe what the drone should be doing 
#state variables are updated by network.py when process() is called and 
#main.py will query these regularly to orient the drone

target = ('','') #lat and long coord set
alt = 50
goal = 0 #values for goal will be defined below
STAY = 0
TRAVEL = 1
RTH = 2
LAND = 3

def updateLocal(msg):
    global target
    global goal
    global alt
    data = msg.split("/")
    target = (data[0],data[1])
    alt = int(data[2])
    goal = int(data[3])

misc.log(misc.info, 'Connecting to P2P Server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
sock.sendto(b'0', server)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        misc.log(misc.info, 'Response OK, waiting for peer')
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

misc.log(misc.info, '\nGot peer')
misc.log(misc.info, '  IP:          {}'.format(ip))
misc.log(misc.info, '  Source port: {}'.format(sport))
misc.log(misc.info, '  Dest port:   {}\n'.format(dport))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', sport))
sock.sendto(b'0', (ip, dport))

misc.log(misc.info, "Connection OK")

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))

    while True:
        data = sock.recv(1024)
        misc.log(misc.info, '\rpeer: {}\n> '.format(data.decode()), end='')
        updateLocal(data.decode())

listener = threading.Thread(target=listen, daemon=True);
listener.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))