import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                break
            print(msg.decode(), end="")
        except:
            break

def main():
    host = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.daemon = True
    thread.start()

    while True:
        try:
            message = input()
            sock.send(message.encode())
        except KeyboardInterrupt:
            print("Disconnected.")
            sock.close()
            break

if __name__ == "__main__":
    main()
