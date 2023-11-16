import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
s.connect(('192.168.1.12', 12345))

# receive data from the server
data = b''
while len(data) < 1024:
    packet = s.recv(1024 - len(data))
    if not packet:
        break
    data += packet

# close the connection
s.close()

# print the received data
print(data)
