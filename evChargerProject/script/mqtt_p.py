# Download the helper library from https://www.twilio.com/docs/python/install
# import os
# from twilio.rest import Client
# # Set environment variables for your credentials
# # Read more at http://twil.io/secure
# account_sid = "AC228c43ee86cd950f5555639ab4cfe90f"
# auth_token = "ffe100df06876701795c553c1a038798"
# client = Client(account_sid, auth_token)
# message = client.messages.create(
#   body="Hello arshad alam, how can y help you!! ",
#   from_="+13156442657",
#   to="+917065564617"
# )
# print(message.sid)

######################################################################################################################################




Conversation opened. 1 unread message.

Skip to content
Using Aviconn Solutions Pvt Ltd Mail with screen readers

1 of 28
Fwd: Pymodbus configuration files and Pymodbus Script code
Inbox

Abhishek Mehra
Attachments
12:46 PM (2 minutes ago)
to me


Thanks and Regards,

Abhishek Mehra,
Software Engineer
Aviconn Solutions Pvt. Ltd.
#510, 5th Floor, Eros City Square,
Rosewood City, Sec-49, Gurugram
Haryana - 122018 

Contact no. - +916005462558




---------- Forwarded message ---------
From: Abhishek Mehra <abhishek.mehra@aviconn.in>
Date: Sat, May 20, 2023 at 11:24 AM
Subject: Fwd: Pymodbus configuration files and Pymodbus Script code
To: Saheb Ali <saheb.ali@aviconn.in>



Thanks and Regards,

Abhishek Mehra,
Software Engineer
Aviconn Solutions Pvt. Ltd.
#510, 5th Floor, Eros City Square,
Rosewood City, Sec-49, Gurugram
Haryana - 122018 

Contact no. - +916005462558




---------- Forwarded message ---------
From: Mandeep Kahlon <mandeep.kahlon@aviconn.in>
Date: Mon, May 15, 2023 at 12:14 PM
Subject: Fwd: Pymodbus configuration files and Pymodbus Script code
To: Abhishek Mehra <abhishek.mehra@aviconn.in>




---------- Forwarded message ---------
From: Mandeep Kahlon <mandeep.kahlon@aviconn.in>
Date: Sat, May 13, 2023 at 5:48 PM
Subject: Pymodbus configuration files and Pymodbus Script code
To: ashishj.1801@gmail.com <ashishj.1801@gmail.com>
Cc: Manish Gupta <manish@aviconn.in>


Dear Sir,

As discussed, PFA files. If you have any query, please let me know.

--
Thanks and Regards,
Mandeep Kaur
Project Manager
Aviconn Solutions Pvt. Ltd.

Contact: +91-7289941981
Email: mandeep.kahlon@aviconn.in



--
Thanks and Regards,
Mandeep Kaur
Project Manager
Aviconn Solutions Pvt. Ltd.

Contact: +91-7289941981
Email: mandeep.kahlon@aviconn.in

3
 Attachments
  •  Scanned by Gmail
Thanks a lot.Thanks for the mail.Done.
from datetime import datetime
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import logging
import csv
import os
from pymodbus.exceptions import ConnectionException

#time.sleep(600)
aECounter=0
cECounter=0
openhab_list = []
wave_items_list = []
poll_time_list = []

with open("newopenhab.csv") as csv_file:
    #print("inside openhab file")
    openhab_conf = csv.reader(csv_file, delimiter='|')
    #print(type(openhab_conf))
    #print("openhab conf array :  : ", openhab_conf)
    next(openhab_conf)
    poll_time = next(openhab_conf)
    poll_time_list.append({"poll_time": poll_time[1]})
    for row in openhab_conf:
        if len(row) == 0:
            break
        else:
            openhab_list.append({"meter_name": row[0], "port": row[1], "baud_rate": int(row[2]), "byte_size": int(row[3]),
                                 "parity": row[4], "stop_bits": int(row[5]), "method": row[6], "timeout": int(row[7]),
                                 "register_type": row[8], "data_type": row[9], "starting_address": int(row[10]),
                                 "length": int(row[11]), "slave_id": int(row[12]), "password": row[13], "pwdEnable": int(row[14])})

    list=len(openhab_list)
    lenOfOpenhab=list*4
    print("Length of openhabList",lenOfOpenhab)
with open("newwaveitems.csv") as csv_file1:
    #print("inside new wave items file")
    wave_items_conf = csv.reader(csv_file1, delimiter='|')
    #print("wave items conf array : ", wave_items_conf)
    next(wave_items_conf)
    for row1 in wave_items_conf:
        if len(row1) == 0:
            break
        else:
            wave_items_list.append({"meter_name1": row1[0], "topic": row1[1], "register": int(row1[2]),
                                    "byte_order": row1[3], "word_order": row1[4]})




def pymodbus_func():
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  Function START $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$") 
    start_time = datetime.now()
    global aECounter
    global cECounter
    print("function start time is : ", start_time) 
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    # time.sleep(int(poll_time))
    for i in openhab_list:
        meter_name = i["meter_name"]
        port = i["port"]
        baud_rate = i["baud_rate"]
        byte_size = i["byte_size"]
        parity = i["parity"]
        stop_bits = i["stop_bits"]
        method = i["method"]
        timeout = i["timeout"]
        register_type = i["register_type"]
        data_type = i["data_type"]
        starting_address = i["starting_address"]
        length = i["length"]
        slave_id = i["slave_id"]
        password = i["password"]
        pwdEnable = i["pwdEnable"]
        try:
            client = ModbusClient(method=method, port=port, baudrate=baud_rate, parity=parity, timeout=timeout,
                                  stopbits=stop_bits, bytesize=byte_size, retries=3, retry_on_empty=True)
            connection=client.connect()
            time.sleep(5)
            if connection==True: 
                print("{} : {} is CONNECTED on portId {}".format(datetime.now(),meter_name,port))
                
            else:
                print(f"Connection is {connection}, socket is {client.is_socket_open()}")
                print("{} : {} is NOT_CONNECTED on portId {}".format(datetime.now(),meter_name,port))
                print("Skipping the Register data read from meter and try next entry of meter from openhabList")
                
            if register_type == "holding":
                #print("inside holding registers")
                #print("Meter Name : ", meter_name)
                register_data = client.read_holding_registers(address=starting_address, count=length, unit=slave_id, password=password,
                                                              pwdEnable=pwdEnable)
                
                #print("register data : ", register_data)

            else:
                print("inside different type of register")
            
            for j in wave_items_list:
                meter_name1 = j["meter_name1"]
                #print("Meter Name inside wave items : ", meter_name1)
                topic = j["topic"]
                register = j["register"]
                register_address = int(register) * 2
                #print("topic : ",topic ,"register mapped :",register, "register address : ",register_address)
                byte_order = j["byte_order"]
                word_order = j["word_order"]
                if meter_name == meter_name1:
                    #print("Inside if condition")
                    if byte_order == "Big":
                        #print("Inside if condition of byte_order")
                        byteorder = Endian.Big
                        #print("byte order : ", byteorder)
                    else:
                        #print("Inside else condition of byte order")
                        byteorder = Endian.Big
                    if word_order == "Big":
                        #print("Inside if condition of word order")
                        wordorder = Endian.Big
                        #print("word order : ", wordorder)
                    else:
                        #print("Inside else condition of word order")
                        wordorder = Endian.Big
                    if data_type == "float32":
                        #print("inside float32 condition")
                        value = BinaryPayloadDecoder.fromRegisters(
                                                        register_data.registers[register_address:register_address + 2],
                                                        byteorder, wordorder)

                        data = float(value.decode_32bit_float())
                        #print("#######################################################")
                        print("{} : Value of {} is : {}".format(datetime.now(),topic, data)) 
                        #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                    else:
                        #print("inside long condition, meter name is {}".format(meter_name1))
                        value = BinaryPayloadDecoder.fromRegisters(register_data.registers[register_address:register_address + 2],
                                                        byteorder, wordorder)
                        data = value.decode_32bit_int()     
                        print("{} : Value of {} is : {}".format(datetime.now(), topic, data)) 
                    if data is not None:
                        mqtt_publish(topic, data)                        

                    else:
                        print("inside disconnected state")
                        data = "Disconnected"
                        mqtt_publish(topic, data)
            
            print("{} : {} has been Connected".format(datetime.now(),meter_name))
            client.close()
            aECounter=0
            cECounter=0           
        

        except ConnectionException as ce:
            print("{} CE ERROR : {}".format(datetime.now(),ce))
            print("{} : {} has been DisConnected on portId {}".format(datetime.now(),meter_name,port))
            client.close()
            cECounter=cECounter+1
            print("cECounter = ",cECounter)
            if cECounter==lenOfOpenhab:
                print("Gateway restarted..........")
                print("Restart System at {} Due to Port Error".format(datetime.now()))
                os.system("echo odroid | sudo -S init 6")


        except AttributeError as ae:
            print("AE ERROR" , ae)
            print("{} : {} has been DisConnected".format(datetime.now(),meter_name))
            client.close()
            aECounter=aECounter+1
            print("aECounter = ",aECounter)
            if aECounter==lenOfOpenhab:
                print("gateway restarted...........")
                print("Restart System at {} Due to Attribute Error".format(datetime.now()))
                os.system("echo odroid | sudo -S init 6")
        except Exception as err:
            print("{} : {} has been Disconnected".format(datetime.now(),meter_name))
            print("Exception inside modbus client connection is : ", err)
 

    end_time = datetime.now()
    print("function end time is : ", end_time)
    time_taken = end_time - start_time
    print("total time taken in seconds is  : ", time_taken.total_seconds()) 
    print("#############################  Function END #######################################")
    return


def mqtt_publish(topic, data):
    #topic_to_send = "/asem/aviconn/1/gateway_id/out/"
    #mqtt_client = mqtt.Client("pymodbus_hub")
    #mqtt_client.connect("127.0.0.1", 1883, 60)
    #print("mqtt client connected")
    #final_topic = topic_to_send + str(topic) + "/state"
    #mqtt_client.publish(final_topic, str(data), qos=2, retain=False)
    value = 'mosquitto_pub -p 5003 -t "/asem/aviconn/54/avc_FMHighBay_BGRBhiwandi_000054_1/out/{}/localstate" -m {}'.format(topic,data)
    os.system(value)
    return


while True:
    print("inside while loop")
    pollTime = poll_time_list[0]["poll_time"]
    time.sleep(int(pollTime))
    pymodbus_func()

openhab_script.py
Displaying openhab_script.py.





