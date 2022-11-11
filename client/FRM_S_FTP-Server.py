import socket
import os
import glob
from math import ceil
from time import sleep
import zipfile
import zlib
import hashlib
import random
import struct
#encrypting functions
#from Crypto.Cipher import AES


def compress(file):
    compressedFile = os.path.splitext(file)[0] + ".zip"
    #if compressedFile exists in current path. use os.path.compressedfile or simething
    fileToZip = zipfile.ZipFile(compressedFile, mode='w', compression=zipfile.ZIP_DEFLATED)
    fileToZip.write(file)
    fileToZip.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '192.168.1.77' #host ip address in quotes
    port = 65432 #listening port in quotes
    username = "admin"
    password =  "a"
    s.bind((host, port))
    s.listen()
    print(host)
    print("waiting for a connection...")
    conn, addr = s.accept()
    print(addr, "Has connected to the server. (incomming ip, from this port)")
    print("connection has been established!")
    
    for x in range(3, 0, -1):
        answer = "\nPlease print your username and password to log into the server. You have " + str(x) + " more tries."
        conn.sendall(answer.encode())
        
        attemptedUsername = conn.recv(2048).decode()
        print(attemptedUsername)
        
        attemptedPassword = conn.recv(2048).decode()
        print(attemptedPassword)
        
        if attemptedUsername == username and attemptedPassword == password:
            sleep(0.1)
            conn.sendall("correct".encode())
            
            while True:
                recieveData = conn.recv(2048).decode()
                print(recieveData)

                if recieveData == 'dir':
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
                    x.sort()
                    string = '\n'.join(x)
                    conn.sendall(string.encode())
                
                elif recieveData == 'ls':
                    x = os.listdir()
                    y = 0
                    x.sort()
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
                        
                elif recieveData[:3] == 'pwd':
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

                    else: 
                        conn.send("Error while reading the file!".encode())
                
                elif recieveData[:4] == 'put ':
                    response = conn.recv(2048).decode()
                    if(response[:4] == 'true'):
                        filesize = int(response[4:])
                        packetAmmount = ceil(filesize/2048)
                        filename = recieveData[4:]
                        if (os.path.isfile('FRM_C_' + filename)):
                            x = 1
                            while(os.path.isfile('FRM_C_' + str(x) + filename )):
                                x += 1
                            f = open('FRM_C_' + str(x) + filename, 'wb')

                        else:
                            f = open("FRM_C_" + filename, 'wb')
                        
                        for x in range (0, packetAmmount):
                            data = conn.recv(2048)
                            f.write(data)
                        
                        f.close()

                elif recieveData[:9] == 'compress ':
                    fileToCompress = recieveData[9:]
                    compress(fileToCompress)
                    conn.send("file specified compressed on server side.".encode())

                elif recieveData == 'quit':
                    x = -1
                    break
            print("disconnected...")
            break
        else:
            sleep(0.1)
            conn.sendall("incorrect".encode())
    
    print("disconnected...")
main()

#https://www.programiz.com/python-programming/methods/string/translate
#https://docs.python.org/3/library/glob.html
#http://net-informations.com/python/pro/sleep.htm
#https://www.youtube.com/watch?v=H8t4DJ3Tdrg
#https://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto
