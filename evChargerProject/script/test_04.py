
import socket
import os
import sys
import json
import time
import django
import requests
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "evChargerProject.settings")
django.setup()

from evChargerProject.evChargerApp.models import Device, Sockets

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 50200
# PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("here")

    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on port {PORT}...")
    while True:
        print("here2222")
        conn, addr = s.accept()
        with conn:
            print(f"Connection established from {addr}")
            Recieved_data = conn.recv(1024)
            print("Received data: ",  Recieved_data)
            received_data_str = Recieved_data.decode(
                'utf-8')  # decode bytes to string
            print("type of data after decode", type(received_data_str))
            try:
                received_data_list = received_data_str.split(";")
                print(received_data_list)
                for d in received_data_list:
                    print('type_data', type(d))
                    print("data", d)
                    data = json.loads(d)
                    print(type(data))
                    def func():
                        r = requests.post("http://192.168.1.39:8000/api/dummyAPi/", data)
                        print("data_save")
                    func()


                device_name = "newd12"
                # device_name=dect_device_name
                device_obj = Device.objects.filter(device_name=device_name)
                Sockets_obj = Sockets.objects.filter(device__in=device_obj)
                print(Sockets_obj)
                rocord_data = []
                rocord_data.append(device_name)
                for sockets_data in Sockets_obj:
                    if sockets_data.is_active is True:
                        status = 1
                        rocord_data.append(status)
                    else:
                        status = 0
                        rocord_data.append(status)
                output_string = rocord_data[0]+"-" + str(rocord_data[1]) + str(
                    rocord_data[2]) + str(rocord_data[3])+"\n"
                print(output_string)
                ack_msg = output_string
                # ack_msg = "newd12-00"
                print("ack_msg", ack_msg)
                encoded_msg = ack_msg.encode()
                print(type(encoded_msg))
                conn.send(encoded_msg)
                print("Send Data: ", ack_msg)
                print("Acknowledgement sent")
                time.sleep(5)
            except Exception as e:
                print(f"Error: {e}")
