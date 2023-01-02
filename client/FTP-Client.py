import socket
import os  #directory related ops
from math import ceil
import sys

def main():
    PORT = int(sys.argv[2])
    HOST = sys.argv[1] 
    s = socket.socket()
    s.connect((HOST, PORT))
 
    authstr = sys.argv[3] + " " + sys.argv[4]
    s.send(authstr.encode())

    answer = s.recv(2048).decode()
    
    if answer == 'correct':
        print("Successful login")
        while True:
            string = input("\ncommand>> ")
            s.sendall(string.encode())

            if string == 'ls':
                x = s.recv(2048).decode()
                print(x)

            elif string == 'rm':
                x = s.recv(2048).decode()
                print(x)

            elif string == 'rename':
                x = s.recv(2048).decode()
                print(x)

            elif string == 'cwd':
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
                        filename = filename.split(".")
                        x = 1
                        while(os.path.isfile('FRM_S_' + filename[0] + str(x) + '.' + filename[1])):
                            x += 1
                        f = open('FRM_S_' + filename[0] + str(x) + '.' + filename[1], 'wb')

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
