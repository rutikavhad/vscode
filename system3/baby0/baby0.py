import socket   # for network communication
import sys      # for command-line arguments
import time     # optional, for adding delays

# ----------------------------
# Step 1: Load configuration
# ----------------------------

def load_config(filename):
    config = {}
    with open(filename, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value
    return config


# ----------------------------
# Step 2: Main program logic
# ----------------------------

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <config_file>")
        sys.exit(1)

    # Load parameters from file
    cfg = load_config(sys.argv[1])

    ear_port = int(cfg['EAR_PORT'])
    mouth_port = int(cfg['MOUTH_PORT'])
    buffer_size = int(cfg['BUFFER_SIZE'])
    remote_ip = cfg['REMOTE_IP']
    remote_ear_port = int(cfg['REMOTE_EAR_PORT'])
    remote_mouth_port = int(cfg['REMOTE_MOUTH_PORT'])

    # ----------------------------
    # Step 3: Create sockets
    # ----------------------------

    # ear_socket will receive messages
    ear_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # mouth_socket will send messages
    mouth_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ----------------------------
    # Step 4: Bind the ear socket
    # ----------------------------

    ear_socket.bind(('', ear_port))
    print(f"System listening (ear) on port {ear_port}...")

    # ----------------------------
    # Step 5: Wait for data
    # ----------------------------

    data, sender_addr = ear_socket.recvfrom(buffer_size)
    message = data.decode()
    print(f"Received from {sender_addr}: {message}")

    # ----------------------------
    # Step 6: Process data
    # ----------------------------

    message += " [processed by system]"

    # ----------------------------
    # Step 7: Send to remote system
    # ----------------------------

    mouth_socket.sendto(message.encode(), (remote_ip, remote_ear_port))
    print(f"Sent processed message to {remote_ip}:{remote_ear_port}")

    # ----------------------------
    # Step 8: Cleanup
    # ----------------------------

    ear_socket.close()
    mouth_socket.close()
    print("Sockets closed. Program ended.")


if __name__ == "__main__":
    main()

