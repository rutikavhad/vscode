import socket
import threading

host = "0.0.0.0"    # correct for localhost
port =55555

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []


def borcast(massage):
    for client in clients:
        client.send(massage)


def handle(client):
    while True:
        try:
            massage=client.recv(1024)
            borcast(massage)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nickname[index]
            borcast(f'{nickname} left the room'.encode('ascii'))
            nicknames.remove(nickname)
            break

def recive():
    while True:
        client,address=server.accept()
        print(f"connected with {str(address)}")
        
        client.send('MATRIX'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')  # single user's nickname
        nicknames.append(nickname)                    # add to the list
        clients.append(client)                        # add client socket


        print(f'nickname of cleaint is {nickname}')
        borcast(f'{nickname}  join a chat'.encode('ascii'))
        client.send('conected to server'.encode('ascii'))

        thread=threading.Thread(target=handle,args=(client,))
        thread.start()

print("server is start to linanig")
recive()
