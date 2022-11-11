import socket
import os  #directory related ops

from math import ceil
from getpass import getpass

def main():
    PORT = 58965
    HOST = '192.168.137.1' 
    s = socket.socket()
    s.connect((HOST, PORT))
    
    message = s.recv(2048).decode()
    print(message)
    
    username = input("username: ")
    s.sendall(username.encode())
    
    print("password: ", end="")
    password = getpass()
    s.send(password.encode())

    answer = s.recv(2048).decode()
    
    if answer == 'correct':
        print("Successful login")
        while True:
            string = input("\ncommand>> ")
            s.sendall(string.encode())

            if string == 'dir':   
                x = s.recv(2048).decode()
                print (x)

            elif string == 'ls':
                x = s.recv(2048).decode()
                print(x)

            elif string == 'rm':
                x = s.recv(2048).decode()
                print(x)

            elif string == 'pwd':
                x = s.recv(2048).decode()
                print(x)

            elif string[:4] == 'get ':
                response = s.recv(2048).decode()
                print(response + ' bytes')
                if(response[:4] == 'file'):
                    filename = string[4:]
                    filesize = int(response[27:])
                    packetAmmount = ceil(filesize/2048)
                    if (os.path.isfile('FRM_S_' + filename)):
                        x = 1
                        while(os.path.isfile('FRM_S_' + str(x) + filename )):
                            x += 1
                        f = open('FRM_S' + str(x) + filename, 'wb')

                    else:
                        f = open("FRM_S_" + filename, 'wb')
                    
                    for x in range (0, packetAmmount):
                        data = s.recv(2048)
                        f.write(data)
                    
                    f.close()
                    print("Download is complete")
                else:
                    print("File does not exist...")
            
            elif string[:4] == 'put ':
                filename = string[4:]
                if os.path.isfile(filename):
                    filesize = int(os.path.getsize(filename))
                    s.sendall(('true' + str(filesize)).encode())
                    with open(filename, 'rb') as f:
                        packetAmmount = ceil(filesize/2048)
                        for x in range(0, packetAmmount):
                            bytesToSend = f.read(2048)
                            s.send(bytesToSend)
                    print("File sent!")
                else:
                    s.sendall('false'.encode())
                    print("File does not exist...")
            
            elif string [:9] == 'compress ':
                x = s.recv(2048).decode()
                print(x)

            elif string == 'quit':
                break

    elif answer == 'disconnect':
        print("WRONG CREDENTIALS! Disconnected!")

main()
