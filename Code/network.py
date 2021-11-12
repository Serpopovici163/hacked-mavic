import socket
import threading
import time

#server related variables
server="http://ludicroustech.ca"
peer_client = None
port=420

#state related variables, these describe what the drone should be doing 
#state variables are updated by network.py when process() is called and 
#main.py will query these regularly to orient the drone

def process(data):
    return data #fix

class Server(threading.Thread):
    def run(self):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname=''
        port=420
        self.sock.bind((hostname,port))
        self.sock.listen(1)
        (master,address)=self.sock.accept()
        while 1:
            process(master.recv(4096))

class Client(threading.Thread):
    def send(self,msg): #as bytes string
        self.sock.send(msg)
    def run(self):
        global server
        global peer_client
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((server,port))
        self.sock.send(b"REQPEER")
        self.sock.listen(1)
        (msg,peer) = self.sock.accept()
        while 1:
            if (msg[0] == b'A'):
                server = msg[2:]
                peer_client=Client()
                peer_client.start()
                break
            else:
                time.sleep(1)

srv=Server()
srv.daemon=True
srv.start()
cli=Client()
cli.start()