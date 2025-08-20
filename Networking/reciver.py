from socket import socket,AF_INET,SOCK_DGRAM
sock=socket(AF_INET,SOCK_DGRAM)
sock.bind(('localhost',6667))

while True:
    msg, addr=sock.recvfrom(8888)
    print("got massasge from %s: %s" %(addr,msg) )