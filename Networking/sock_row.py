#!/use/bin/env python
from socket import socket, AF_PACKET,SOCK_RAW
s=socket(AF_PACKET,SOCK_RAW)
s.bind(("eth1",0))

