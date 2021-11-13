import socket
import sys, traceback
import threading
import select

SOCKET_LIST=[]
PEER_LIST=[]
SENT_BY={}

host = ''
port = 420

class Server(threading.Thread):

    def init(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.bind((host,port))
        self.sock.listen(2)
        SOCKET_LIST.append(self.sock)

    def run(self):
        while 1:
            read,write,err=select.select(SOCKET_LIST,[],[],0)     
            for sock in read:
                if sock==self.sock:                    
                    sockfd,addr=self.sock.accept()
                    SOCKET_LIST.append(sockfd)
                else:
                    try:
                        s=sock.recv(1024)
                        if s=='REQPEER':
                            print(str(sock.getpeername()))                            
                            continue
                        else:
                            PEER_LIST.append(sock.getpeername())  
                            SENT_BY[s]=(str(sock.getpeername()))
                    except:
                        print(str(sock.getpeername()))                  
                    
class handle_connections(threading.Thread):
    def run(self):        
        while 1:
            read,write,err=select.select([],SOCKET_LIST,[],0)
            for items in PEER_LIST:
                for s in write:
                    try:
                        if(str(s.getpeername()) != SENT_BY[items]):
                            s.send(items)                                         
                    except:
                        traceback.print_exc(file=sys.stdout)
                PEER_LIST.remove(items)   
                del(SENT_BY[items])              
                


if __name__=='__main__':
    srv=Server()
    srv.init()
    srv.start()
    print(SOCKET_LIST)
    handle=handle_connections()    
    handle.start()   

