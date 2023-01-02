#FTP works on a client-server model. The FTP client is a program that runs on the user’s computer to enable the user to talk to and get files from remote computers.

import socket
import os
from math import ceil
import zipfile
import datetime as dt

def timelo():
    time = str(dt.datetime.now()).split(".")
    time = time[0]
    return time

def connection(conn, addr):
        logs = open('C:/Users/yash/Desktop/cn_project_fin_asli/logs.txt', "a")
        
        constr= timelo() + " " + str(addr)+ " connected\n"
        logs.write(constr)
        while True:
            recieveData = conn.recv(2048).decode()
            print(recieveData)

            if recieveData == 'ls':
                x = os.listdir()
                y = 0
                for file in x:
                    if os.path.isfile(file):
                        string = 'F: ' + str(file) 
                        x[y] = string
                    else:
                        string = 'D: ' + str(file)
                        x[y] = string
                    y += 1
                string = '\n'.join(x)
                conn.sendall(string.encode())
            
            elif recieveData[:2] == 'rm':
                file_path = os.getcwd() + '\\' + recieveData[3:]
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    constr = timelo() + " " + recieveData[3:] + " has been deleted\n"
                    logs.write(constr)
                else:
                    print("File does not exist")

            elif recieveData[:6] == 'rename':
                recieveData = recieveData.split()
                file_path = os.getcwd() + '\\' + recieveData[1]
                if os.path.isfile(file_path):
                    os.rename(recieveData[1], recieveData[2])
                    constr= timelo() + " " + "Renamed " + recieveData[1] + " as " + recieveData[2] + "\n"
                    logs.write(constr)
                else:
                    print("File does not exist")

            elif recieveData[:2] == 'cd':                    
                if recieveData[:3] == 'cd ':
                    wantedPath = os.getcwd() + '\\' + recieveData[3:]                        
                    if os.path.exists(wantedPath):
                        os.chdir(wantedPath)
                elif recieveData[2:4] == '..':
                    currentPath = os.getcwd()
                    list = currentPath.split('//')
                    list.remove(-1)
                    wantedPath = '//'.join(list)
                    os.chdir(wantedPath)
                    
            elif recieveData[:3] == 'cwd':
                string = str(os.getcwd())
                conn.sendall(string.encode())

            elif recieveData[:4] == 'get ':
                filename = recieveData[4:]
                if os.path.isfile(filename):
                    conn.sendall(("file exists with a size of " + str(os.path.getsize(filename))).encode())
                    filesize = int(os.path.getsize(filename))
                    with open(filename, 'rb') as f:
                        packetAmmount = ceil(filesize/2048)
                        for x in range(0, packetAmmount):
                            bytesToSend = f.read(2048)
                            conn.send(bytesToSend)
                    constr = timelo() + " " + "get " + filename + "\n"
                    logs.write(constr)

                else: 
                    conn.send("Error while reading the file!".encode())
            
            elif recieveData[:4] == 'put ':
                response = conn.recv(2048).decode()
                if(response[:4] == 'true'):
                    filesize = int(response[4:])
                    packetAmmount = ceil(filesize/2048)
                    filename = recieveData[4:]
                    if (os.path.isfile('FRM_C_' + filename)):
                        filename = filename.split(".")
                        x = 1
                        while(os.path.isfile('FRM_C_' + filename[0] + str(x) + '.' + filename[1])):
                            x += 1
                        f = open('FRM_C_' + filename[0] + str(x) + '.' + filename[1], 'wb')

                    else:
                        f = open("FRM_C_" + filename, 'wb')
                    
                    for x in range (0, packetAmmount):
                        data = conn.recv(2048)
                        f.write(data)
                    
                    f.close()
                    constr = timelo() + " " + "put " + filename + "\n"
                    logs.write(constr)

            elif recieveData[:9] == 'compress ':
                fileToCompress = recieveData[9:]
                compress(fileToCompress)
                conn.send("file specified compressed on server side.".encode())
                constr = timelo() + " " + "compressed " + recieveData[9:] + "\n"
                logs.write(constr)

            elif recieveData == 'quit':
                x = -1
                break
        print("disconnected...")
        constr = timelo() + " " + "disconnected\n\n"
        logs.write(constr)
        logs.close()

def main():
    soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #tcp socket
    
    host = '10.100.107.39' 
    port = 58965
    username = "remoteadmin"
    password =  "read"
    soket.bind((host, port))
    soket.listen()
    print(host)
    print("waiting for a connection...")
    conn, addr = soket.accept()
    
    unpa = conn.recv(2048).decode()
    un_pa = unpa.split()
    un = un_pa[0]
    pa = un_pa[1]
    print(un)
    
    if un == username and pa == password:
        conn.sendall("correct".encode())
        print(addr, "Has connected to the server.")
        connection(conn, addr)
    
    else:
        conn.sendall("incorrect".encode())
        print("disconnected")

def compress(file):
    compressedFile = os.path.splitext(file)[0] + ".zip"
    file_to_be_zipped = zipfile.ZipFile(compressedFile, mode='w', compression=zipfile.ZIP_DEFLATED)
    file_to_be_zipped.write(file)
    file_to_be_zipped.close()

main()

