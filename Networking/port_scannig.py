# this program for scan only open ports

import socket
import threading
from queue import Queue
 

target="10.31.56.76"

quequ=Queue()
open_port=[]


def port_scan(port):
    try:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((target,port))
        return True
    except:
     return False
    


def fill_queue(port_list):
   for port in port_list:
      quequ.put(port)

def worker():
   while not quequ.empty():
      port=quequ.get()
      if port_scan(port):
         print("port {} is open",format(port))
         open_port.append(port)
    #   else:
    #       print("port {}is closed",formatf)        
port_list=range(1,1024)
fill_queue(port_list)
thread_list=[]

for t in range(100):
   thread=threading.Thread(target=worker)
   thread_list.append(thread)

for  thread in thread_list:
   thread.start()

for thread in thread_list:
   thread.join()

print("open port {} ",open_port)

    
# for port in range(1,1024):
#    result=port_scan(port)
#    if result:
#       print("port {} open",format(port))
#    else:
#       print("port {}close",format(port))
   