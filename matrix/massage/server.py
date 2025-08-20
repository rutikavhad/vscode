import socket
import threading

# Configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345
PASSWORD = "mypassword"
clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    try:
        client_socket.send(b"Enter password: ")
        password = client_socket.recv(1024).decode().strip()
        if password != PASSWORD:
            client_socket.send(b"Incorrect password. Connection closed.\n")
            client_socket.close()
            return

        client_socket.send(b"Welcome to the chat server!\n")
        clients.append(client_socket)

        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            broadcast(msg, client_socket)
    finally:
        client_socket.close()
        if client_socket in clients:
            clients.remove(client_socket)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
