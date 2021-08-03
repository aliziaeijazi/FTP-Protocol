from socket import *
import os ,time , random , datetime

MainRoot = os.getcwd()
os.chdir("File")
RootDir = os.getcwd()

def Help(_Connection):
    HelpDoc = "[+]HELP:            Show this help\n" + \
              "[+]LIST:            List of files\n" + \
              "[+]PWD :            Show current dir\n" + \
              "[+]CD dir name :    Change directory\n" + \
              "[+]DWLD file_path:  Download File\n" + \
              "[+]QUIT:            Exit\n" 
    _Connection.sendall(HelpDoc.encode())
    return "HelpDoc is sended Successfully. :: " +  str(datetime.datetime.now())

def List(_Connection):
    FileList=os.listdir(os.getcwd())
    TotalDirectorySize = 0
    List = "List Files : \n"
    for i in FileList:
        if os.path.isdir(i):
            List += "> " + i + "   -  " + str(os.stat(i).st_size) + "b\n"
        else:
            List += i + "   -  " + str(os.stat(i).st_size) + "b\n"
        TotalDirectorySize += os.stat(i).st_size
    List+="Total size of This Directory : " + str(TotalDirectorySize) + "b\n"
    _Connection.sendall(List.encode())
    return "FileList is sended Successfully. :: " +  str(datetime.datetime.now()) 

def Pwd(_Connection):
    Path = os.path.relpath(os.getcwd() , RootDir)
    if Path == ".":
        Path = "\\"
    elif Path[0] != "\\":
        Path = "\\" + Path
    _Connection.sendall(Path.encode())
    return "FilePath is sended Successfully. :: " +  str(datetime.datetime.now()) 

def Cd(_Connection , _Command):
    DirChange = _Command.split()[1]
    if os.path.isdir(DirChange):
        if DirChange == "..":
            Address , temp = os.path.split(os.getcwd())
            if Address == MainRoot:
                _Connection.sendall("This Dir is Root.".encode())
                return "Access Violation. :: " +  str(datetime.datetime.now())
            else:
                os.chdir(Address)
                Path = os.path.relpath(os.getcwd() , RootDir)
                if Path == ".":
                    Path = "\\"
                elif Path[0] != "\\":
                    Path = "\\" + Path
                Path = "Directory changed to : " + Path
                _Connection.sendall(Path.encode())
                return "Directory changed to : " + Path + "Successfully. :: " +  str(datetime.datetime.now())
        else:
            os.chdir(DirChange)
            Path = os.path.relpath(os.getcwd() , RootDir)
            if Path == ".":
                Path = "\\"
            elif Path[0] != "\\":
                Path = "\\" + Path
            Path = "Directory changed to : " + Path
            _Connection.sendall(Path.encode())
            return "Directory changed to : " + Path + "Successfully. :: " +  str(datetime.datetime.now())
    else:
        DirChange += " not fount."
        _Connection.sendall(DirChange.encode())
        return "Failed." + DirChange + " :: " +  str(datetime.datetime.now())


def Dwld(_Connection , _Command):
    FileName = _Command.split()[1]
    if os.path.isfile(FileName):
        _Connection.sendall("Accept".encode())
        print("Server is send " + FileName +  str(datetime.datetime.now()))
        Start_Time = time.time()
        FTPServerName = "127.0.0.1"
        FTPServerPort = random.randint(3000,50000)
        _Connection.sendall(str(FTPServerPort).encode())
        FTPSocket = socket(AF_INET , SOCK_STREAM)
        FTPSocket.bind((FTPServerName , FTPServerPort))
        FTPSocket.listen()
        FTPConnection , FTPClientAddress = FTPSocket.accept()
        File = open(FileName , "rb")
        FileContent=File.read()
        File.close()
        FTPConnection.sendall(FileContent)
        FTPConnection.close()
        End_Time = time.time()
        Detail = "Download Succssfully.   File Size : " + str(os.stat(FileName).st_size) + "b     Time of Downloading : " + str( End_Time - Start_Time)
        _Connection.sendall(Detail.encode())
        return FileName + "is Sending Successfully. :: " + str(datetime.datetime.now())
    else:
        FileName += " is not Found."
        _Connection.sendall(FileName.encode())
        return FileName+" :: " + str(datetime.datetime.now())

def Exit():
    return "this Connection disconnected. :: " + str(datetime.datetime.now())

def Commands(_Connection , _Command):
    _Connection.sendall("This Command is incorrect.".encode())
    return "Type incorrect Command : " + _Command + " :: " + str(datetime.datetime.now())

def Main():
    print("Wellcome! This is a FTP Server")
    ServerName = "127.0.0.1"
    ServerPort = 2121
    print("Server is ready...\nServer is listening on Nmae : " + str(ServerName) + "& Port : " + str(ServerPort) + \
          "\nWaiting to get Request from Client")
    ServerSocket = socket(AF_INET , SOCK_STREAM)
    ServerSocket.bind((ServerName,ServerPort))
    ServerSocket.listen(6)
    Connection , ClientAddress = ServerSocket.accept()
    print("A Client With Address : " + str(ClientAddress) + "Connected")
    print("Date And Time of Connecting this Client : " + str(ClientAddress) + " :: " + str(datetime.datetime.now()))
    print("listennig for get Commands :")
    while True:
        Command = Connection.recv(1024).decode()
        print("\nCommand Recived : " + Command + " :: " + str(datetime.datetime.now()))
        if Command.split()[0].lower() == "help":
            print(Help(Connection))
        elif Command.split()[0].lower() == "list":
            print(List(Connection))
        elif Command.split()[0].lower() == "pwd":
            print(Pwd(Connection))
        elif Command.split()[0].lower() == "cd":
            print(Cd(Connection , Command))
        elif Command.split()[0].lower() == "dwld":
            print(Dwld(Connection , Command))
        elif Command.split()[0].lower() == "quit":
            print(Exit())
        else:
            print(Commands(Connection , Command))


Main()