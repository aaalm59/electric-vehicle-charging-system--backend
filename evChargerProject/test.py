import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 50200
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((TCP_IP, TCP_PORT))
print("connected: ", s)
data = s.recv(BUFFER_SIZE)
s.close()
print("received data: ", data)
