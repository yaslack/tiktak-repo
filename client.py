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
                message = input("Your Turn : ")
                if message == "":
                    message = "rien"
                client_socket.send(message.encode())  # send message
            elif data == "Wait":
                print("Wait for your Turn ...")
        if player == 2:
            data = client_socket.recv(1024).decode()
            if data == "Play P2":
                message = input("Your Turn : ")
                if message == "":
                    message = "rien"
                client_socket.send(message.encode())  # send message

            elif data == "Wait":
                print("Wait for your Turn ...")

    message = "exit"
    client_socket.send(message.encode())
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()