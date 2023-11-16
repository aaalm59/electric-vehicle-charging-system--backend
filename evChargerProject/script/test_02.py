import socket
# Define host and port
HOST = ''
PORT = 50201
# Create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to host and port
server_socket.bind((HOST, PORT))
# Listen for incoming connections
server_socket.listen()
# Accept incoming connections and process data
while True:
    # Accept incoming connection
    conn, addr = server_socket.accept()
    # Process incoming data
    with conn:
        print('Connected by', addr)
        while True:
            # Receive data from client
            data = conn.recv(1024)
            if not data:
                break
            # Process data
            print(data)
            conn.close()