from pickle import FALSE
import socket,sys,itertools, threading, time, sys
import signal,os

def real_handler(signum, frame, arg1):
    message = "exit"
    arg1.send(message.encode())
    exit(1)



def client_program():

    host = sys.argv[1]  # as both code is running on same pc
    port = 7777  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    signal.signal(signal.SIGINT, lambda signum, frame: real_handler(signum, frame, client_socket))

    message = ""  # take input
    data = client_socket.recv(1024).decode()  # receive response

    player = 0

    if data == "Maximum reached":
        print("Maximum Player reached Disconnection")
        sys.exit()
    elif data == "Wait":
        print("Wait for Second Player ...")
        player= 1
    elif data == "Second":
        print("Wait for your Turn ...")
        player = 2

    while message.lower().strip() != 'bye':
        if player == 1:
            data = client_socket.recv(1024).decode()
            if data == "Play P1":
                print('Generating the board ...')
                tab = client_socket.recv(1024).decode()
                print(tab)
                message=""
                while(True):
                    message = input("Your Turn : ")
                    if(message.isdigit()):
                        if(0 <= int(message) <= 8):
                            break
                    print("You need to enter a number between 0 and 8\n")
                    print(tab)
                    
                client_socket.send(message.encode())  # send message
            elif data == "Wait":
                print("Wait for your Turn ...")
            elif data == "over":
                print('Generating the board ...')
                print("Game Over")
                tab = client_socket.recv(1024).decode()
                print(tab)
                break
        if player == 2:
            data = client_socket.recv(1024).decode()
            if data == "Play P2":
                print('Generating the board ...')
                tab = client_socket.recv(1024).decode()
                print(tab)
                message=""
                while(True):
                    message = input("Your Turn : ")
                    if(message.isdigit()):
                        if(0 <= int(message) <= 8):
                            break
                    print("You need to enter a number between 0 and 8\n")
                    print(tab)
                client_socket.send(message.encode())  # send message

            elif data == "Wait":
                print("Wait for your Turn ...")
            elif data == "over":
                print('Generating the board ...')
                print("Game Over")
                tab = client_socket.recv(1024).decode()
                print(tab)
                break

    message = "exit"
    client_socket.send(message.encode())
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()