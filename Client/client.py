from socket import *

ServerName = "127.0.0.1"

def Help(_ClientSocket,_Command):
    print("Requesting Help ...")
    _ClientSocket.sendall(_Command.encode())
    return _ClientSocket.recv(1024).decode()

def List(_ClientSocket,_Command):
    print("Requesting List ...")
    _ClientSocket.sendall(_Command.encode())
    return _ClientSocket.recv(1024).decode()

def Pwd(_ClientSocket,_Command):
    print("Requesting Path ...")
    _ClientSocket.sendall(_Command.encode())
    return _ClientSocket.recv(1024).decode()

def Cd(_ClientSocket,_Command):
    print("Changing dir to : " + _Command.split()[1])
    _ClientSocket.sendall(_Command.encode())
    return _ClientSocket.recv(1024).decode()

def Dwld(_ClientSocket , _Command):
    _ClientSocket.sendall(_Command.encode())
    Detail =_ClientSocket.recv(1024).decode()
    if Detail == "Accept":
        FTPServerPort = _ClientSocket.recv(1024).decode()
        FTPSocket = socket(AF_INET , SOCK_STREAM)
        FTPSocket.connect((ServerName , int(FTPServerPort)))
        File = open(_Command.split()[1] , "wb")
        FileContent  = b""
        while True:
            Temp = FTPSocket.recv(1024)
            if Temp:
                FileContent += Temp
            else:
                break
        FTPSocket.close()
        File.write(FileContent)
        File.close()
        return _ClientSocket.recv(1024)
    else:
        return Detail

def Command(_ClientSocket,_Command):
    print("Requesting ???? ")
    _ClientSocket.sendall(_Command.encode())
    return _ClientSocket.recv(1024).decode()

def Exit(_ClientSocket , _Command):
    _ClientSocket.sendall(_Command.encode())
    _ClientSocket.close()
    return _ClientSocket.recv(1024).decode()





def Main():
    ServerPort = 2121
    print("Connecting to Server...\nPlease Wait.....\n")
    ClientSocket = socket(AF_INET , SOCK_STREAM)
    try:
        ClientSocket.connect((ServerName,ServerPort))
        print("Connecting successful.\nWellcome to the FTP Client")
    except:
        print("Connecting Failed!\n")
    print(Help(ClientSocket,"help"))
    while True:
        InputCommand = input("\nYour Command:> ")
        if InputCommand.split()[0].lower() == "help":
            print(Help(ClientSocket , InputCommand))
        elif InputCommand.split()[0].lower() == "list":
            print(List(ClientSocket , InputCommand))
        elif InputCommand.split()[0].lower() == "pwd":
            print(Pwd(ClientSocket , InputCommand))
        elif InputCommand.split()[0].lower() == "dwld":
            print(Dwld(ClientSocket , InputCommand))
        elif InputCommand.split()[0].lower() == "cd":
            print(Cd(ClientSocket , InputCommand))
        elif InputCommand.split()[0].lower() == "quit":
            print(Exit(ClientSocket , InputCommand))
            return 0
        else:
            print(Command(ClientSocket , InputCommand))
            
Main()
