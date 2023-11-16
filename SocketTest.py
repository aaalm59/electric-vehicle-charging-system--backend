# # import socket
# # import requests
# # import json
# # from evChargerProject.evChargerApp.models import Sockets

# # HOST = ''   # Symbolic name meaning all available interfaces
# # PORT = 50200

# # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# #     print("here")

# #     s.bind((HOST, PORT))
# #     s.listen()
# #     print(f"Listening on port {PORT}...")

# #     conn, addr = s.accept()
# #     if conn:
# #         print(f"Connection established from {addr}")

# #         Device = "Device1"

# #         Socket = Sockets.objects.filter(device=Device)
# #         print(Socket)

# #         data = conn.recv(1024)
# #         print("Received data: ", data)

# import os
# import sys
# import socket
# import requests
# import json

# import django
# BASE_DIR = os.path.dirname(os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__))))       
# sys.path.append(BASE_DIR)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE",
#                       "evChargerProject.settings")  
# django.setup()



# from evChargerProject.evChargerApp.models import Device, Sockets

# device_obj=Device.objects.filter(device_name="Device2")
# Sockets_obj=Sockets.objects.filter(device__in=device_obj)
# print(Sockets_obj)
# rocord_data=[]
# rocord_data.append('Device2')
# for sockets_data in Sockets_obj:
#     if sockets_data.is_active is True:
#         status=1
#         rocord_data.append(status)
#     else:
#         status=0
#         rocord_data.append(status)

# output_string = rocord_data[0]+"/" + str(rocord_data[1]) + str(rocord_data[2]) + str(rocord_data[3])+"\n"
# print(output_string)
    


    # socket_data=i.socket
    # print(socket_data)
    # device=i.device
    # print(device)
    # is_active = i.is_active
    # print(is_active)
    # if is_active is False:
    #     off_false=0
    #     print(off_false)
    # else:
    #     on_true=1

# if is_active is False:
#     off_false=0
#     data=f"{device}/{off_false}"
# elif 