import socket
import threading
#debug
import time
import os

host = ''
port = 420
peer1 = None
peer2 = None

class Server(threading.Thread):
    def run(self):
        global peer1
        global peer2
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host,port))
        self.sock.listen(1)
        (master,address)=self.sock.accept()
        while 1:
            #debug
            os.system("cls")
            if (peer1 != None):
                print("Peer1 > " + str(peer1))
            else:
                print("Peer1 > None")
            if (peer2 != None):
                print("Peer2 > " + str(peer2))
            else:
                print("Peer2 > None")
            #endDebug
            msg = master.recv(4096)
            if (msg == b"REQPEER"):
                if (peer1 != None and peer2 != None): #ditch conf in case DISCON was not sent
                    peer1 = None
                    peer2 = None
                
                if (peer1 == None):
                    peer1 = address
                    self.sock.send(b"WAIT")
                elif (address == peer1 and peer2 != None):
                    self.sock.send(b"A:" + peer2)
                elif (peer2 == None and address != peer1):
                    peer2 = address
                    self.sock.send(b"A:" + peer1)
                else:
                    self.sock.send(b"WAIT")
            elif (msg == b"DISCON" and (address == peer1 or address == peer2)): #discon clause
                peer1 = None
                peer2 = None

srv = Server()
srv.daemon = True
srv.start()            