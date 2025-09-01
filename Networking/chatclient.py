'''

if windows : ipconfig -look for IPv4 Address : put in :client.connect(('..*..',55555))
if linux : ifconfig - look for  inet         : put in :client.connect(('..*..',55555))



'''

import socket
import threading
nickname=input("enter yourname")
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(('10.31.56.76', 55555))
def receive():
    while True:
        try:
            massage=client.recv(1024).decode('ascii')
            if massage=="MATRIX":
                pass
            else:
                print(massage)
        except:
            print("error found")
            client.close()
            break

def write():
    while True:
        massage=(f'{nickname} {input("")}')
        client.send(massage.encode('ascii'))

recive_thread=threading.Thread(target=receive)
recive_thread.start()

write_thread=threading.Thread(target=write)
write_thread.start()