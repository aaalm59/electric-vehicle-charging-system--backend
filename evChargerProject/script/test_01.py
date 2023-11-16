import socket
import random
import time
HOST = ''
PORT = 50207
num_sockets = 3
sockets_data = []
# dum_list=['{"deviceId":"newd12", "socketId":1, "voltage":234, "Current":0.02, "Energy":0.00, "Status":"OF",  "total_time":"0008"}', '{"deviceId":"newd12", "socketId":2, "voltage":234, "Current":0.02, "Energy":0.00, "Status":"OF",  "total_time":"0004"}', '{"deviceId":"newd12", "socketId":3, "voltage":234, "Current":0.02, "Energy":0.00, "Status":"OF",  "total_time":"0002"}\n']
for i in range(num_sockets):
  voltage = round(random.uniform(0, 10), 4)
  current = round(random.uniform(0, 5), 4)
  deviceId = 'newd12'
  socketId=i+1
  Energy = round(random.uniform(0, 5), 3)
  Status = (random.randint(0, 1))
  total_time= 0000
  if Status == 1:
    Status='ON'
    total_time+= 30
    print('total_time',total_time)
  else:
    Status='OF'
    total_time+=0
  print('total_time',total_time)
  print("main function called")
  
  total_time = str(round(random.uniform(0, 9), 4))
  sockets_data.append({'deviceId':deviceId, 'voltage': voltage, 'Current': current,'Energy':Energy,'socketId':socketId,'total_time':total_time})
print(sockets_data)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send(sockets_data.encode())
response = client_socket.recv(1024).decode()
print(response)
time.sleep(1)
client_socket.close()