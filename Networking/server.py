import socket
import sys

def create_socket():
    try:
        global host
        global port
        global soc
        host = ""
        port = 9998
        soc = socket.socket()

    except socket.error as msg:
        print("socket creation error" + str(msg))


#binding a socket and  listning a conections

def bind_socket():
    try:
        global host
        global port
        global soc
        print("binding a port number " + str(port))  
        soc.bind((host, port))                      
        soc.listen(5)                               
    except socket.error as msg:
        print("socket binding error" + str(msg) + "\n" + "retry...")
        bind_socket()

#make a connection with a cleint using a socket

def socet_accept():
    conn, address = soc.accept()
    print("connection has been establish" + "ip" + address[0] + "| and port is " + str(address[1]))
    send_command(conn)

    conn.close()

#send a command to frinds 
def send_command(conn):
    while True:
        cmd = input()
        if cmd == "exit":
            conn.close()
            soc.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))

            client_responce = str(conn.recv(1024), "utf-8")
            print(client_responce, end=" ")

def main():
    create_socket()
    bind_socket()
    socet_accept()

main()
