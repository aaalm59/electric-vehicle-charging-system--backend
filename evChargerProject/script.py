import time
import requests
import json

# #data = {"name":"Aviconn"}
Recieved_data = b'{"deviceId":"newd12", "socketId":1, "voltage":251, "Current":2.02, "Energy":0.00, "Status":"ON",  "total_time":"0000"};{"deviceId":"newd12", "socketId":2, "voltage":251, "Current":1.02, "Energy":0.00, "Status":"OF",  "total_time":"0000"};{"deviceId":"newd12", "socketId":3, "voltage":251, "Current":1.02, "Energy":0.00, "Status":"OF",  "total_time":"0000"}\n'
print("Raw_data_recieved_type:  " ,type(Recieved_data))
received_data_str = Recieved_data.decode('utf-8')  # decode bytes to string
# print(received_data_str)
print("type of data after decode",type(received_data_str))

received_data_list=received_data_str.split(";")
print(received_data_list)
print("type of data after split:  ",type(received_data_list))
while True:
    for d in received_data_list:
        data = json.loads(d)
        print(type(data))
        print(data)
        
        def func():
            r = requests.post("http://192.168.1.12:8000/api/dummyAPi/",data)
            print("here")
            return r.json()

        func()
    # # def func():
    #     r = requests.post("http://192.168.1.12:8000/api/dummyAPi/",received_data_dict)
    #     print("here")
    time.sleep(5)
        

# data = {"deviceId":"newd12", "socketId":1, "voltage":251, "Current":2.02, "Energy":0.00, "Status":"ON",  "total_time":"0000"}






