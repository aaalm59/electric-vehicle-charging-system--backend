import socket
import random

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a specific IP address and port
s.bind(('192.168.1.12', 50201))

# listen for incoming connections
s.listen(1)

# accept a connection
conn, addr = s.accept()

# generate 1024 bytes of random data
data = bytes([random.randint(0, 255) for _ in range(1024)])

# send the random data to the client
conn.send(data)

# close the connection
conn.close()
import socket
import random

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a specific IP address and port
s.bind(('192.168.1.12', 50201))

# listen for incoming connections
s.listen(1)

# accept a connection
conn, addr = s.accept()

# generate 1024 bytes of random data
data = bytes([random.randint(0, 255) for _ in range(1024)])

# send the random data to the client
conn.send(data)

# close the connection
conn.close()
