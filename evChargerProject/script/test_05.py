import select
import socket
import threading
import time

def handle_data(device_socket):
    while True:
        data = device_socket.recv(1024)
        if not data:
            # Remove socket from the list
            sockets_list.remove(device_socket)
            del devices_data[device_socket]
            break
        else:
            devices_data[device_socket] += data

def print_data():
    while True:
        time.sleep(5)
        for device, data in devices_data.items():
            print("------------------------------------------Top-------------------------------------------------------")
            print(f"Data from device at {device.getpeername()}: {data}")
            print('---------------------------------------------------------------------------------------------')

# Define host and port
HOST = ''
PORT = 50200

# Create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to host and port
server_socket.bind((HOST, PORT))
# Listen for incoming connections
server_socket.listen()

# List of sockets to monitor
sockets_list = [server_socket]
# Dictionary to store data from each device
devices_data = {}

# Create a separate thread to print data
print_thread = threading.Thread(target=print_data)
print_thread.start()

while True:
    # Call select function to monitor sockets
    read_sockets, _, _ = select.select(sockets_list, [], [], 1)
    # Iterate over sockets with data ready to be read
    for sock in read_sockets:
        # If new connection, accept it
        if sock == server_socket:
            conn, addr = server_socket.accept()
            sockets_list.append(conn)
            devices_data[conn] = b''
            # Create a separate thread to handle data for each device
            data_thread = threading.Thread(target=handle_data, args=(conn,))
            data_thread.start()
