import socket
import threading

#server related variables
host="http://ludicroustech.ca"
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
    def connect(self,host,port):
        self.sock.connect((host,port))
    def send(self,msg): #as bytes string
        self.sock.send(msg)
    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect(host,port)

srv=Server()
srv.daemon=True
srv.start()
cli=Client()
cli.start()