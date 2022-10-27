# !/ usr / bin / python3
from grid import *
import socket,select,signal,random,atexit


@atexit.register
def lastCall():
    print('GoodBye')

def disconnect(l,ss):
    l.remove(ss)
def sendUsers(l,ss,arg):
    for user in l:
        if user != ss:
            user.sendall(arg.encode('utf-8'))
def sendUser(ss,arg):
    ss.sendall(arg.encode('utf-8'))

def real_handler(signum, frame, arg1):
    print("\nClosing Server")
    arg1.close()
    print("Server Closed")
    exit(1)

def main():
    grids = [grid(), grid(), grid()]
    current_player = J1

    l = []
    print('Opening server')
    s = socket . socket ( socket . AF_INET6 , socket . SOCK_STREAM , 0)
    s.setsockopt ( socket . SOL_SOCKET , socket . SO_REUSEADDR , 1)
    s.bind (('',7777))
    s.listen (1)
    signal.signal(signal.SIGINT, lambda signum, frame: real_handler(signum, frame, s))
    print('Server Opened')
    maxPlayer =2
    currentPlayer = 0
    while True :
        l1,l2,l3 = select.select(l+[s],[],[])
        for ss in l1:
            if ss == s :
                if len(l) == 0 :
                    news, a = s.accept()
                    newConnect = 'client connected "'+str(a[0])+':'+str(a[1])+'"'
                    print("Player 1 Connected")
                    news.sendall(b"Wait")
                    l.append(news)
                elif len(l) == 1:
                    news, a = s.accept()
                    newConnect = 'client connected "'+str(a[0])+':'+str(a[1])+'"'
                    print("Player 2 Connected")
                    news.sendall(b"Second")
                    l.append(news)
                    sendUsers(l,ss,"Play P1")
                    currentPlayer = 1
                else:
                    news, a = s.accept()
                    print("New Player rejected")
                    news.sendall(b"Maximum reached")
            else:
                c = ss.recv(1000)
                if c.decode('utf-8') == "exit":
                    disconnect(l,ss)
                if currentPlayer == 1:
                    sendUsers(l,ss,"Play P2")
                    sendUser(ss,"Wait")
                    currentPlayer = 2
                elif currentPlayer == 2:
                    sendUsers(l,ss,"Play P1")
                    sendUser(ss,"Wait")
                    currentPlayer = 1
    s.close()
main()