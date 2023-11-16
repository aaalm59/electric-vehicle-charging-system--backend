        

import os
import sys
import json
import time
import django
import requests
import socket

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))       
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","evChargerProject.settings")  
django.setup()

from evChargerProject.evChargerApp.models import Device, Sockets

while True:
    dum_list=['{"deviceId":"newd12", "socketId":1, "voltage":234, "Current":0.02, "Energy":0.00, "Status":"ON",  "total_time":"0008"}', '{"deviceId":"newd12", "socketId":2, "voltage":234, "Current":0.02, "Energy":0.00, "Status":"OF",  "total_time":"0004"}', '{"deviceId":"newd12", "socketId":3, "voltage":234, "Current":0.02, "Energy":0.00, "Status":"ON",  "total_time":"0002"}\n']
    for d in dum_list:
            print('type_data',type(d))
            print("data",d)
            data = json.loads(d)
            print(type(data))
            # # dect_device_name=data['deviceId']

            # # print("dect_data",dect_device_name)
            def func():
                r = requests.post("http://192.168.1.12:8000/api/dummyAPi/",data)
                # r.json()
                print("here")
                # return r.json()

            func()
            # # print("data_rec>>>>>>>>>>",data)

    device_name="newd12"
    # device_name=dect_device_name
    device_obj=Device.objects.filter(device_name=device_name)
    Sockets_obj=Sockets.objects.filter(device__in=device_obj)
    print(Sockets_obj)
    rocord_data=[]
    rocord_data.append(device_name)
    for sockets_data in Sockets_obj:
        if sockets_data.is_active is True:
            status=1
            rocord_data.append(status)
        else:
            status=0
            rocord_data.append(status)
    output_string = rocord_data[0]+"-" + str(rocord_data[1]) + str(rocord_data[2]) + str(rocord_data[3])+"\n"
    print(output_string)
    ack_msg = output_string
    time.sleep(5)
    