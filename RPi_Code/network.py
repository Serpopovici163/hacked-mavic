import socket
import os
import threading
from typing import runtime_checkable
import misc

#debug
import time

#server related variables
server=("ludicroustech.ca", 55555)

#state related variables, these describe what the drone should be doing 
#state variables are updated by network.py when process() is called and 
#main.py will query these regularly to orient the drone

sock = None
ip = ""
sport = 0
dport = 0
target = ('','') #lat and long coord set
alt = 50

def updateLocal(msg):
    global target
    global alt
    data = msg.split("/")
    target = (data[0],data[1])
    alt = int(data[2])

def listen():
    global sock
    while True:
        try:
            data = sock.recv(1024)
            misc.log(misc.info, '\rpeer: {}\n> '.format(data.decode()), end='')
            updateLocal(data.decode())
        except:
            pass #bad thing ik but it's fine since I'm expecting Timeout errors here

def connect():
    global dport
    misc.log(misc.info, 'Connecting to P2P Server')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 50001))
    sock.settimeout(5)
    
    running = True
    while running:
        try:
            sock.sendto(b'0', server)
            data = sock.recv(1024).decode()
            if data.strip() == 'ready':
                misc.log(misc.info, 'Response OK, waiting for peer')
                running = False
        except:     
            running = True   

    running = True
    while running:
        try:
            data = sock.recv(1024).decode()
            running = False
        except:
            running = True

    ip, sport_str, dport_str = data.split(' ')
    sport = int(sport_str)
    dport = int(dport_str)

    misc.log(misc.info, 'Got peer')
    misc.log(misc.info, '  IP:          {}'.format(ip))
    misc.log(misc.info, '  Source port: {}'.format(sport))
    misc.log(misc.info, '  Dest port:   {}'.format(dport))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))
    sock.sendto(b'0', (ip, dport))

    misc.log(misc.info, "Connection OK")

    listener = threading.Thread(target=listen, daemon=True)
    listener.start()

def ping():
    url,port=server
    if (os.system("ping -c 1 " + url) == 0):
        return True
    else:
        return False

def init():
    if (ping()):
        connect()
        return True
    return False

#debug
connect()
try:
    while True:
        listen()
        time.sleep(1)
except KeyboardInterrupt:
    print("ctrl-c")