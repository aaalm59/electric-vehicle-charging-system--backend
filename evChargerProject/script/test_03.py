import socket
import os
import sys
import json
import time
import django
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "evChargerProject.settings")
django.setup()

from evChargerProject.evChargerApp.models import Device, Sockets

HOST = ''
PORT = 50200

# Django setup
django.setup()

# Retrieve device and socket objects
device_name = "newd12"
device_obj = Device.objects.filter(device_name=device_name)
sockets_obj = Sockets.objects.filter(device__in=device_obj)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on port {PORT}...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connection established from {addr}")

            received_data = conn.recv(1024)
            received_data_str = received_data.decode('utf-8')

            received_data_list = received_data_str.split(";")
            for d in received_data_list:
                data = json.loads(d)
                r = requests.post("http://192.168.1.39:8000/api/dummyAPi/", data)
                print("Data saved")

            rocord_data = [device_name]
            for sockets_data in sockets_obj:
                status = 1 if sockets_data.is_active else 0
                rocord_data.append(status)

            output_string = "-".join(map(str, rocord_data)) + "\n"
            print(output_string)

            ack_msg = output_string
            encoded_msg = ack_msg.encode()
            conn.send(encoded_msg)
            print("Send Data:", ack_msg)
            print("Acknowledgement sent")

        time.sleep(5)
