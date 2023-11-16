# data = [{'deviceId': 'newd12', 'voltage': 5.3495, 'Current': 1.7633, 'Energy': 4.802, 'socketId': 1, 'total_time': 0}, {'deviceId': 'newd12', 'voltage': 9.743, 'Current': 2.2476, 'Energy': 0.804, 'socketId': 2, 'total_time': 30}, {'deviceId': 'newd12', 'voltage': 9.9936, 'Current': 1.0158, 'Energy': 2.94, 'socketId': 3, 'total_time': 0}]

# result = []

# for item in data:
#     result.append(f'{{"deviceId":"{item["deviceId"]}", "socketId":{item["socketId"]}, "voltage":{item["voltage"]}, "Current":{item["Current"]}, "Energy":{item["Energy"]}, "Status":"OF", "total_time":"{str(item["total_time"]).zfill(4)}"}}')

# print(result)
# print(type(result))


data = b"[{'deviceId': 'newd12', 'voltage': 5.4196, 'Current': 4.9521, 'Energy': 2.789, 'socketId': 1, 'total_time': 30}, {'deviceId': 'newd12', 'voltage': 8.5781, 'Current': 0.0246, 'Energy': 1.932, 'socketId': 2, 'total_time': 30}, {'deviceId': 'newd12', 'voltage': 3.8631, 'Current': 3.7925, 'Energy': 2.784, 'socketId': 3, 'total_time': 30}]"

# Convert bytes to string and then parse as list of dictionaries
parsed_data = eval(data.decode("utf-8"))
# print(parsed_data)
# print('parsss',type(parsed_data))

# Convert the list of dictionaries to the desired format
formatted_data = [f'{{"deviceId":"{d["deviceId"]}", "socketId":{d["socketId"]}, "voltage":{d["voltage"]:.2f}, "Current":{d["Current"]:.2f}, "Energy":{d["Energy"]:.2f}, "Status":"OF", "total_time":"{d["total_time"]:04}"}}' for d in parsed_data]

for i in formatted_data:
    print('data',i)

# print(formatted_data)
# print(type(formatted_data))

