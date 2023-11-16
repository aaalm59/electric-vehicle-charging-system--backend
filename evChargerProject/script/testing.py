import socket
import random
import json
import time
import threading

HOST = '192.168.1.39'
PORT = 50200

devices = [
    {"id": "newd11", "interval": 30},
    {"id": "newd12", "interval": 20},
    {"id": "newd13", "interval": 10},
    {"id": "newd14", "interval": 5},
    {"id": "newd15", "interval": 15},
    {"id": "newd16", "interval": 40},
    {"id": "newd17", "interval": 25},
    {"id": "newd18", "interval": 35},
    {"id": "newd19", "interval": 10},
    {"id": "newd20", "interval": 15}
]

def generate_socket_data(device_id, socket_id):
    voltage = round(random.uniform(0, 10), 4)
    current = round(random.uniform(0, 5), 4)
    energy = round(random.uniform(0, 5), 3)
    status = random.randint(0, 1)
    total_time = 0 if status == 0 else 30
    return {
        "deviceId": device_id,
        "voltage": voltage,
        "Current": current,
        "Energy": energy,
        "socketId": socket_id,
        "total_time": total_time,
        "Status": "ON" if status == 1 else "OF"
    }

def send_data(device):
    while True:
        sockets_data = [generate_socket_data(device['id'], i) for i in range(1, 4)]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            data_str = json.dumps(sockets_data)
            print(data_str)
            client_socket.send(data_str.encode())
        time.sleep(device['interval'])

# Create a thread for each device
threads = []
for device in devices:
    thread = threading.Thread(target=send_data, args=(device,))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()
