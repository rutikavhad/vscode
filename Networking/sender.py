#!/usr/bin/env python
from socket import socket,AF_INET,SOCK_DGRAM
s=socket(AF_INET,SOCK_DGRAM)
s.connect(('localhost',6667))
s.send(b'hello')
s.close()
