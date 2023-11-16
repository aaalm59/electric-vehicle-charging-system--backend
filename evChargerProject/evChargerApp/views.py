from datetime import timedelta, datetime, time
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from evChargerProject.evChargerApp.models import ConsumerHistory, DailyPropertyReading, Device, Property, SocketLiveData, Sockets
from rest_framework import viewsets, status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
# from tutorial.quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db.models import Sum, Avg, Max, Min, Count
from django.db.models import Case, CharField, Value, When
from .models import *
from .serializers import *
import time
from django.db.models import Q
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    User = get_user_model()
    queryset = User.objects.all().order_by('-date_joined')
    # serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    # serializer_class = GroupSerializer


def entryExit(aFunc):
    """Trace entry, exit and exceptions."""

    def loggedFunc(*args, **kw):
        print('*********************')
        print('enter In Function : {} at {} '.format(aFunc.__name__, str(time.strftime('%I:%M:%S %p'))))
        try:
            result = aFunc(*args, **kw)
            print("These are the arguments {} and results {}".format(args, result))
        except Exception as e:
            print('exception in {}  and {}'.format(aFunc.__name__, e))

        print('exit from Function : {} at {} '.format(aFunc.__name__, str(time.strftime('%I:%M:%S %p'))))
        print('*********************')
        return result

    loggedFunc.__name__ = aFunc.__name__
    loggedFunc.__doc__ = aFunc.__doc__
    return loggedFunc


class LoginApi(APIView):
    def post(self, request):
        print("hii")
        print("login data", request.data)
        mobile_number = request.data.get("mobile_number")
        if mobile_number:
            print("inside new project condition")
            generate_otp = 123
            check_user = User.objects.filter(Contact_number=mobile_number)
            print("check user : ", check_user)
            if check_user.exists():
                user_status = True
                token, created = Token.objects.get_or_create(user=check_user[0])
                return Response({"status": 200, "otp": generate_otp, "user_status": user_status, "token": token.key,
                                 "user": {"id":check_user[0].id, "UserType": check_user[0].UserType, "username": check_user[0].first_name}})
            else:
                print("user not exist")
                user_status = False
                # User.objects.create(Contact_number=mobile_number)
                return Response({"status": 200, "otp": generate_otp, "user_status": user_status})

        else:
            return Response({'msg': "user not exist "})


class RegisterData(APIView):
    def post(self, request):
        data = request.data
        print("data : ", data)
        username = data.get("username",None)
        email = data.get("email",None)
        mobile = data.get("mobile")
        user_type = data.get("userType")
        check_user = User.objects.filter(Contact_number=mobile)
        print("check_user: ", check_user)
        try:
            if check_user.exists():
                check_user.update(first_name=username, email=email, UserType=user_type)
                print("user updated")
            else:
                User.objects.create(first_name=username, email=email, UserType=user_type, Contact_number=mobile)
                print("user created")
                check_user = User.objects.get(Contact_number=mobile)
                Wallet.objects.create(username=username,user=check_user)
            token, created = Token.objects.get_or_create(user=check_user[0])
            print("token : ", check_user)
            print("user type : ", check_user[0].UserType)
            return Response({"status": 200, "token": token.key, "user": {"id":check_user[0].id, "UserType": check_user[0].UserType, "username": check_user[0].first_name}})
        except Exception as err:
            print("err:fefdvdvdvdvdrv ", err)
            return Response({"status": 500})

class ValidatedToken(APIView):
    def post(self, request):
        data = request.data
        print("data is: ", data)
        token = data.get("token", '')
        print("token is :", token)
        user = Token.objects.filter(key=token)
        if user.exists():
            return Response({"result": "true"})
        else:
            return Response({"result": "false"})



class FetchAllCustomers(APIView):
    def get(self, request   ):
        customers = User.objects.filter(UserType=4)
        customer_data_list = []
        if customers.exists():
            for i in customers:
                customer_data_list.append({"id": i.id, "username": i.username, "email": i.email})
        return Response({"status": 200, "msg": "customer details", "data": customer_data_list})


class FetchProperties(APIView):
    def post(self,request):
        data = request.data
        user_id = data.get("user_id")
        user=User.objects.get(id=user_id)
        property_info = Property.objects.filter(user=user)
        if not property_info.exists():
            property_info = Property.objects.filter(manager=user)
        list = []
        for i in property_info:
            print("cmndmc: ", i.manager)
            if i.manager:
                list.append({"id": i.id,"propertyName":i.property_name,"full_address":i.full_address,"location":i.location,
                             "totalDevices":i.total_no_of_devices,
                             "manager": i.manager.first_name,"mobileNumber":i.manager.Contact_number})
            else:
                list.append({"id": i.id, "propertyName": i.property_name,"full_address":i.full_address, "location": i.location,
                             "totalDevices": i.total_no_of_devices, "manager": ""})
        return Response({"status":200,"data":list})


# class PropertyDetailsAdd(APIView):
#     def post(self,request):
#        data = request.data
#        user_id = data.get("user_id")
#        propertyName = data.get("propertyName")
#        location = data.get("location")
#        user = User.objects.get(id=user_id)
#        property = Property.objects.create(user=user,property_name=propertyName,location=location)
#        return Response({"status":200, "msg":"Data saved sucessfully"})


class CreateProperty(APIView):
    def post(self, request):
        data = request.data
        print("data : ", data)
        user_id = data.get("userId")
        propertyData = data.get("propertyData")
        propertyName = propertyData["propertyName"]
        propertyAddress = propertyData["full_address"]
        location = propertyData["location"]
        try:
            user = User.objects.get(id=user_id)
            Property.objects.create(user=user, property_name=propertyName, full_address=propertyAddress,location=location)
            return Response({"status": 200})
        except Exception as err:
            print("Error ", err)
            return Response({"status": 500})


class CreateManager(APIView):
    def post(self, request):
        data = request.data
        managerName = data.get("managerName")
        managerEmail = data.get("managerEmail")
        mobile = data.get("contactNumber")
        propertyId = data.get("property")
        property = Property.objects.filter(id=int(propertyId))
        try:
            if property.exists():
                user = User.objects.create(first_name=managerName, email=managerEmail, Contact_number=mobile, UserType=5)
                print("user : ", user)
                property.update(manager=user)
                return Response({"status": 200})
            else:
                return Response({"status": 500, "msg":"property not created"})

        except Exception as err:
            print("Error ", err)
            return Response({"status": 500})


class AddDevice(APIView):
    def post(self, request):
        data = request.data
        device = data.get("deviceId")  
        propertyId = data.get("property")
        socket = data.get("socketId")
        try:
            property = Property.objects.get(id=int(propertyId))
            device = Device.objects.create(property=property, device_name=device)
            deviceCount=Device.objects.filter(property=property).count()
            print("deviceCount",deviceCount)
            property = Property.objects.filter(id=int(propertyId)).update(total_no_of_devices=deviceCount)
            for socket_no in range(1, 4):
                Sockets.objects.create(device=device, socket=socket_no)
            return Response({"status": 200})
        except Exception as err:
            print("Error ", err)
            return Response({"status": 500})

class FetchDevice(APIView):
    def post(self, request):
        data = request.data
        print("data : ", data)
        propertyId = data.get("propertyId")
        try:
            allDevice = Device.objects.filter(property=int(propertyId))
            data = []
            for device in allDevice:
                socket = Sockets.objects.filter(device=device.id)
                allSocketData = []
                for i in socket:
                    allSocketData.append({"socketName": i.get_socket_display(), "id": i.id, "socketStatus": i.is_active})
                data.append({"deviceName": device.device_name, "deviceId": device.id, "allSocket": allSocketData})
            return Response({"status": 200, "data": data})
        except Exception as err:
            print(err)
            return Response({"status": 500, "data":[]})


# class LiveDataApi(APIView):
#     def post(self,request):
#         data = request.data
#         print("data : ",data)
#         deviceId = data.get("deviceId")
#         print("deviceId :", deviceId)
#         socketId = data.get("socketId")
#         print("socketId :", socketId)
#         status = data.get("Status",'')
#         print("status : ",status)
#         device = Device.objects.get(device_name=deviceId)
#         print("device", device)
#         property = device.property.property_name
#         print("property: ", property)
#         location = device.property.full_address
#         print("location", location)
#         if status =="ON":
#             print("socket On now")
#             device=Device.objects.filter(device_name=deviceId)
#             print("device : ",device)
#             deviceName = Device.objects.get(device_name=deviceId)
#             socket = Sockets.objects.filter(device__in=device, socket=socketId)
#             socketName = socket[0].id
#             socketID = Sockets.objects.get(id=socketName)
#             print("socketNAME%%%%%%%",socketID)
#             Socket_Live_Data_obj = SocketLiveData.objects.order_by('socket').last()
#             sockert_id=Socket_Live_Data_obj.id
#             Socket_Live_Data = SocketLiveData.objects.get(id=sockert_id)
#             socketList = []
#             socketList.append({"totalTime": Socket_Live_Data.total_time, "current": Socket_Live_Data.current, "voltage": Socket_Live_Data.voltage,"unit_consumption": Socket_Live_Data.unit_consumption, "url_field": Socket_Live_Data.url_field})
#             totalamount = Socket_Live_Data.unit_consumption * 10
#             print("socketList",socketList)
#             return Response({"status":200,"propertyName":property,"amount":totalamount,"propertyLocation":location,"deviceName":device.device_name,"socketNumber":socketId,"data":socketList})


class EnergyMonthyTrendApi(APIView):
    def post(self,request):
        data=request.data
        print("Data :",data)
        propertyId = data.get("propertyId")
        deviceId = data.get("deviceId")
        current_date = datetime.now()
        previous_date = current_date - timedelta(days=1)
        previous_month_year = current_date.strftime("%Y-%m")
        property = Property.objects.get(id=propertyId)
        print(property)
        month_list = []
        energy_consumed_list = []
        if property and not deviceId:
            print("inside if")
            devices = Device.objects.filter(property=property)
            print("device :",devices)
            for device in devices:
                consumption_list = []
                for i in range(11, -1, -1):
                    month = current_date - timedelta(i * 364 / 12)
                    print("month%%%%", month)
                    print("month##### : ", month.date())
                    date_in_str = month.strftime('%b')
                    year_in_str = month.strftime("%Y")
                    modified_date = date_in_str + "-" + year_in_str
                    month_list.append(modified_date)
                    month_year = month.strftime("%Y-%m")
                    print("month_year", month_year)
                    socket_list=Sockets.objects.filter(device=device)
                    socket_list = [s.id for s in socket_list]
                    print("socket_list:",socket_list)
                    daily=DailyPropertyReading.objects.filter(property_id=property,socket__in=socket_list, reading_for__month=month.month, reading_for__year=month.year)
                    print("daily:",daily)
                    energyConsumed = 0.0
                    if daily.exists:
                        for j in daily:
                            energyConsumed = j.unit_consumption
                    consumption_list.append(energyConsumed)
                energy_consumed_list.append({"name": device.device_name, "data": consumption_list})
        else:
            print("socket data !!!!!!!!@@@@@@@@@@@@@@@@@@@@@@@")
            device = Device.objects.get(id=deviceId)
            socket = Sockets.objects.filter(device=device)
            for s in socket:
                consumption_list = []
                for i in range(11, -1, -1):
                    month = current_date - timedelta(i * 364 / 12)
                    print("month%%%%", month)
                    print("month##### : ", month.date())
                    date_in_str = month.strftime('%b')
                    year_in_str = month.strftime("%Y")
                    modified_date = date_in_str + "-" + year_in_str
                    month_list.append(modified_date)
                    month_year = month.strftime("%Y-%m")
                    print("month_year", month_year)
                    daily = DailyPropertyReading.objects.filter(property_id=property, socket=s,
                                                                reading_for__month=month.month,
                                                                reading_for__year=month.year)
                    print("daily:", daily)
                    energyConsumed = 0.0
                    if daily.exists:
                        for j in daily:
                            energyConsumed = j.unit_consumption
                    consumption_list.append(energyConsumed)
                energy_consumed_list.append({"name": s.get_socket_display(), "data": consumption_list})
        return Response({"status":200,"months": month_list,"data":energy_consumed_list})


class FetchConsumerSelectedDeviceInfo(APIView):
    def post(self, request):
        data = request.data
        print("data : ", data)
        deviceId = data.get("deviceId")
        deviceData = Device.objects.filter(device_name=deviceId)
        print("device data : ", deviceData)
        if deviceData.exists():
            socketData = Sockets.objects.filter(device=deviceData[0].id)
            print(socketData)
            allSocketData = []
            for i in socketData:
                allSocketData.append({"socketName": i.get_socket_display(), "id": i.id, "socketStatus": i.is_active})
            print(allSocketData)
            finalData = {"deviceName": deviceId, "propertyId": deviceData[0].property.id, "status": 200, "allSocket": allSocketData}
            return Response(finalData)
        else:
            return Response({"status": 500})


class EnergySavingMonthlyBarChart(APIView):
    def post(self, request):
        t1 = time.time()
        print("initial time : ", t1)
        data = request.data
        print("data : ", data)
        propertyId = data.get("propertyId", '')
        property = Property.objects.get(id=propertyId)
        from_date = data.get("from_date", '')
        till_date = data.get("till_date", '')
        fromDate = datetime.strptime(from_date, "%Y/%m/%d")
        tillDate = datetime.strptime(till_date, "%Y/%m/%d")
        dateList = []
        dataList = []
        all_device_id = Device.objects.filter(property=property)
        for deviceId in all_device_id:
            print("deviceId : ", deviceId)
            all_socket_id = Sockets.objects.filter(device=deviceId.id)
            dateList = []
            unitConsumptionList = []
            daily_data = DailyPropertyReading.objects.filter(property_id=property, socket__in=all_socket_id)
            for i in range(7):
                date = tillDate - timedelta(days=6 - i)
                print("date : ", date)
                dateList.append(date.date())
                unit_consumption = 0.0
                daily = daily_data.filter(reading_for__date=date.date())
                print("daily : ", daily)
                if daily.exists():
                    for j in daily:
                        unit_consumption += j.unit_consumption
                unitConsumptionList.append(round(unit_consumption, 2))
            name = deviceId.device_name
            dataList.append({"name": name, "data": unitConsumptionList, 'type': 'column'})
        t2 = time.time()
        print("final time : ", t2)
        print("total time taken : ", t2 - t1)
        return Response({"result": 1, "Dates": dateList, "Data": dataList})


class ConsumerBillApi(APIView):
    def post(self,request):
        data=request.data
        print("data")
        socketId = data.get("socketId")
        print("socketId :", socketId)
        propertyId = data.get("propertyId")
        socket = SocketLiveData.objects.filter(socket=socketId)
        property = Property.objects.get(id=propertyId)
        propertyName = property.property_name
        # propertyLocation = property.location
        # deviceName = socket[0].device.device_name
        socketNumber = socket[0].socket.socket
        amount=10
        socketList = []
        for i in socket:
            socketList.append({"unit_consumption": i.unit_consumption})
            totalamount=i.unit_consumption*10
        return Response({"status": 200, "propertyName": propertyName, "amount":totalamount,"data": socketList})


# class ConsumerHistoryApi(APIView):
#     def post(self,request):
#         data=request.data
#         print("data : ",data)
#         userId = data.get('user_id','')
#         property=Property.objects.get(user=userId)
#         try:
#             if property.exists:
#                 list=[]
#                 history=ConsumerHistory.objects.filter(property=property)
#                 print("history : ",history)
#                 for i in history:
#                     list.append({"propertyName":i.property.property_name,"location":i.property.location,
#                                  "date":i.date,"eneryConsumed":i.unit_consumed})
#                 return Response({"status":200,"data":list})
#         except Exception as err:
#             print("Error ", err)
#             return Response({"status": 500})

class ConsumerHistoryApi(APIView):
    def post(self,request):
        data=request.data
        print("data",data)
        userId = data.get('user_id','')
        consumer=User.objects.get(id=userId)
        history = ConsumerHistory.objects.filter(consumer=consumer)
        list=[]
        for i in history:
            list.append({"propertyName":i.property,"location":i.location,"DeviceID":i.deviceId,
                                 "date":i.date,"eneryConsumed":i.unit_consumed})
        return Response({"status":200,"data":list})


class SocketOnApi(APIView):
    def post(self,request):
        data = request.data
        print("data :",data)
        userId = data.get("userId")
        deviceId = data.get("deviceId")
        print("Device@@@@",deviceId)
        socketId = data.get("socketId")
        print('socketId',socketId)
        user = User.objects.get(id=userId)
        device = Device.objects.get(device_name=deviceId)
        print("device", device)
        property = device.property.property_name
        print("property: ", property)
        location = device.property.full_address
        print("location", location)
        list = {}
        socketON=Sockets.objects.filter(device=device,id=socketId).update(user=userId,is_active = True,status="ON",pending_Command="ON")

        print("socketON>>>>>", socketON)
        if socketON:
            print("here")
            consumerHistory = ConsumerHistory.objects.create(consumer=user,deviceId=deviceId,property=property,location=location)
            list["deviceId"] = deviceId,
            list['socketId'] = socketId,
            list['status'] = 'ON'
        return Response({"status": 200, "msg": "Request for Socket ON","data":list})


class SocketOffApi(APIView):
    def post(self,request):
        print("herre")
        data = request.data
        print("data>>>",data)
        deviceId = data.get("deviceId")
        socketId = data.get("socketId")
        device=Device.objects.get(device_name=deviceId)
        print("device",device)   
        socketON=Sockets.objects.filter(device=device,socket=socketId).update(user=None,
                                                                              status="OFF",pending_Command="OFF",is_active=False)
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("socketON", socketON)
        return Response({"status": 200, "msg": "Socket is off now"})


class CheckSocketUsedByUser(APIView):
    def post(self, request):
        data = request.data
        userId = data.get('userId')
        checkSocketUsedByUser = Sockets.objects.filter(user=userId, status="ON")
        print(checkSocketUsedByUser)
        if checkSocketUsedByUser.exists():
            device = Device.objects.filter(id=checkSocketUsedByUser[0].device.id)
            print("device : ", device)
            return Response({"status": 200, "socketId": checkSocketUsedByUser[0].socket, "deviceId": checkSocketUsedByUser[0].device.device_name,
                             "propertyId": device[0].property.id})
        return Response({"status": 404})

class dummyAPi(APIView):
    def post(self,request):
        data = request.data
        print("response>>>>>",data)
        deviceId=data.get('deviceId')
        print("deviceId : ",deviceId)
        socketId=data.get("socketId",'')
        print("socketId : ",socketId)
        voltage = data.get("voltage",'')
        print("voltage : ",voltage)
        current = data.get("Current",'')
        energy = data.get("Energy",'')
        total_time = data.get("total_time","")
        print("Total_time: ",total_time)
        print(type(total_time))
        # reading_from = data.get("Reading_from",'')
        # reading_to = data.get("Reading_to",'')
        # print("reading_to",reading_to)
        status = data.get("Status",'')
        print("status : ",status)
        url = "http://192.168.1.41/mjpeg/1"
        if status =="ON":
            print("socket On now")
            device=Device.objects.filter(device_name=deviceId)
            print("device_LIST>>>: ",type(device))
            deviceName = Device.objects.get(device_name=deviceId)
            socket = Sockets.objects.filter(device__in=device, socket=socketId)
            print("socket>>>",socket)
            # socket.update(is_active=True,status=status)
            socketid = socket[0].id
            socketID = Sockets.objects.get(id=socketid)# remove
            print("socket%%%%%%%",socket)
            s=SocketLiveData.objects.create(device=deviceName,socket=socketID,socket_Id=socketid,voltage=voltage,current=current,unit_consumption=energy,
                    total_time=total_time,url_field=url)
            property = deviceName.property.property_name
            propertyName = Property.objects.get(property_name=property)
            print("property%%%%", property)
            DailyPropertyReading.objects.create(property_id=propertyName, device=deviceName, socket=socketID,
                                                unit_consumption=energy)
            print("Daily entry created successfully")
        elif status=="OF":
            print("Socket Off now")
            device = Device.objects.filter(device_name=deviceId)
            print("device : ", device)
            deviceName = Device.objects.get(device_name=deviceId)
            socket = Sockets.objects.filter(device__in=device, socket=socketId)
            socketName = socket[0].id
            socketID = Sockets.objects.get(id=socketName)
            s = SocketLiveData.objects.filter(device=deviceName, socket=socketID).delete()
        elif status=="NL":
            device = Device.objects.filter(device_name=deviceId)
            print("device : ", device)
            deviceName = Device.objects.get(device_name=deviceId)
            socket = Sockets.objects.filter(device__in=device, socket=socketId)
            socket_no=socketId[-1]
            print("socket_no==============",socket_no)
            socketName = socket[0].id
            print('socketName',socketName)
            socketID = Sockets.objects.get(id=socketName)
            # socket_id=socketID.socket
            # print('type________________-',type(socket_id))
            # print('socket_id--------',socket_id)
            s = SocketLiveData.objects.filter(device=deviceName, socket=socketID).delete()
            socket.update(user=None,status="OFF",pending_Command="OFF",is_active=False)
            data={"deviceId":deviceName,"socketId":socket_no}
            print(data)
            def func():
                r = requests.post(
                    "http://192.168.1.39:8000/api/socketOffApi/", data)
                return r
                print("data_save;;;;;;;;;;;")

            func()

        else:
            print("error in socket Data")
        return Response({"status": 200,"msg":"Data saved successfully"})

data={"DeviceId":234,"SocketId":2,"Voltage":230,"Energy":2.34,"Status":"ON"}

# class LiveDataApi(APIView):
#     def post(self,request):
#         data = request.data
#         print("data : ",data)
#         Status = data.get("Status")
#         if Status == 'ON':
#             DeviceID = data.get("deviceId")
#             print("DeviceID:", DeviceID)
#             SocketID = data.get("socketId")
#             print("SocketId:", SocketID)
#             socket_name = SocketLiveData.objects.filter()
#             print(socket_name)
#         # # 
        
#         # propertyId = data.get("propertyId")
#         # print("propertyId###",propertyId)
#         # socket = SocketLiveData.objects.filter(id = 46)
#         # if socket.exists():
#         #     print("socket",socket)
           
#         #     #     deviceName = socket[0].device.device_name
#         #     #     print("deviceName", deviceName)
#         #     #     socketNumber = socket[0].socket.socket
#         #     socketList = []
#         #     for i in socket:
#         #         socketList.append({"totalTime": i.total_time, "current": i.current, "voltage": i.voltage,
#         #                                "unit_consumption": i.unit_consumption, "url_field": i.url_field})
#         #         totalamount = i.unit_consumption * 10
#         #     # except Exception as err:
#         #     #     print(err)
#         #     #     totalamount = 0
#         #     #     socketList = []
#         # else:
#         #     totalamount = 0
#         #     socketList = []

#         property = Property.objects.get(id=propertyId)
#         propertyName = property.property_name
#         propertyLocation = property.location
#         print("propertyLocation",propertyLocation)
#         print(socketList)
#         return Response({"status":200,"propertyName":propertyName,"amount":totalamount,"propertyLocation":propertyLocation,"deviceName":socketData.device.device_name,
#                          "socketNumber":socketData.socket,"data":socketList})
    
# class LiveDataApi(APIView):
#     def post(self,request):
#         data = request.data
#         print("data><><><><><",data)
#         socketId = data.get("socketId")
#         print("socketId :", socketId)
#         socketData = Sockets.objects.get(id=socketId)
#         print("socketData: ", socketData)
#         propertyId = data.get("propertyId")
#         print("propertyId###",propertyId)
        
#         socket = SocketLiveData.objects.filter(id="282")
#         if socket.exists():
#             print("socket",socket)
#             # try:
#             #     date=socket[0].reading_from
#             #     date1=socket[0].reading_to
#             #     total=str(date1-date)
#             #     totalTime=datetime.strptime(total, '%H:%M:%S')
#             #     print("totalTime#########",totalTime)
#             #     deviceName = socket[0].device.device_name
#             #     
# print("deviceName", deviceName)
#             #     socketNumber = socket[0].socket.socket
#             socketList = []
#             for i in socket:
#                 socketList.append({"totalTime":i.total_time, "current": i.current, "voltage": i.voltage,
#                                        "unit_consumption": i.unit_consumption, "url_field": i.url_field})
#                 totalamount = i.unit_consumption * 10

#             print("socketlist>>>>>>",socketList)
#             # except Exception as err:
#             #     print(err)
#             #     totalamount = 0
#             #     socketList = []
#         else:
#             totalamount = 0
#             socketList = []

#         property = Property.objects.get(id=propertyId)
#         propertyName = property.property_name
#         propertyLocation = property.location
#         print("propertyLocation",propertyLocation)

#         return Response({"status":200,"propertyName":propertyName,"amount":totalamount,"propertyLocation":propertyLocation,"deviceName":socketData.device.device_name,
#                          "socketNumber":socketData.socket,"data":socketList})

class LiveDataApi(APIView):
    def post(self,request):
        data = request.data
        print("data><><><><><",data)
        socketId = data.get("socketId")
        print("socketId :", socketId)
        socketData = Sockets.objects.get(id=socketId)
        print("socketData: ", socketData)
        propertyId = data.get("propertyId")
        print("propertyId###",propertyId)
        socket = SocketLiveData.objects.filter(socket_Id=socketId).last()
        socketList = []
    
        if socket:
            print("ifCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
            socketList.append({"totalTime": socket.total_time, "current": socket.current, "voltage": socket.voltage,"unit_consumption": socket.unit_consumption, "url_field": socket.url_field})
            totalamount = socket.unit_consumption * 10
            
            
        else:
            print("elseEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            totalamount = 0
            socketList.append({"totalTime":0, "current": 0, "voltage": 0,
                                        "unit_consumption": 0, "url_field": 0})

        property = Property.objects.get(id=propertyId)
        propertyName = property.property_name
        propertyLocation = property.location
        print("propertyLocation",propertyLocation)
        print(socketList)

        return Response({"status":200,"propertyName":propertyName,"amount":totalamount,"propertyLocation":propertyLocation,"deviceName":socketData.device.device_name,
                         "socketNumber":socketData.socket,"data":socketList})


import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from .paytm import *

class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print("data><><><><><",data)
        amount = data.get("amount")
        headers = {'Content-type': 'application/json'}
        merchant_id = 'LAbpsM05367248471551'
        merchant_key = '86w0T0Bw45zLT7yU'
        data = {
            'mid': merchant_id,
            'orderId': 'order_id_12345',
            'txnAmount': str(amount),
            'website': 'WEBSTAGING',
            'industryType': 'Retail',
            'channelId': 'WEB',
            'callbackUrl': 'http://localhost:8000/api/payment/callback/',
            'custId': 'customer_id_12345',
        }
        data['CHECKSUMHASH'] =generate_checksum(data, merchant_key)
        print(data)
        # send a request to Paytm's server to initiate the payment transaction
        response = requests.post('https://securegw-stage.paytm.in/order/process/', headers=headers, json=data)
        return JsonResponse(response.json())

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        # Process payment response here
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})



class Start_payment(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        # request.data is coming from frontend
        amount = data.get("amount")
        headers = {'Content-type': 'application/json'}

        # amount = request.data['amount']
        # name = request.data['name']
        # email = request.data['email']

        # we are saving an order instance (keeping isPaid=False)
        # order = Order.objects.create(product_name=name,
        #                              order_amount=amount,
        #                              user_email=email, )

        # serializer = OrderSerializer(order)
        # we have to send the param_dict to the frontend
        # these credentials will be passed to paytm order processor to verify the business account
        param_dict = {
            'MID': 'LAbpsM05367248471551',
            'ORDER_ID': 'order_123',
            'TXN_AMOUNT': str(amount),
            'CUST_ID': 'aaa@gmail.com',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://localhost:8000/api/payment/callback/',
            # this is the url of payment/callback/ function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
        }

        # create new checksum (unique hashed string) using our merchant key with every paytm payment
        param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, '86w0T0Bw45zLT7yU')
        print('param_dict',param_dict)
        # send the dictionary with all the credentials to the frontend
        # response = requests.post('https://securegw-stage.paytm.in/order/process/', headers=headers, json=param_dict)
        # print(response)
        # return JsonResponse(response.json())
        return Response({'param_dict': param_dict})
    
# class Property_Search_location(APIView):
#     def post(self, request):
#         data = request.data
#         keyword = data.get("keyword")
#         properties_list = []
        
#         if keyword:
#             # Validate keyword length
#             if len(keyword) < 3:
#                 return Response({'error': 'Keyword length must be at least 3 characters'})
            
#             try:
#                 properties = Property.objects.filter(Q(location__icontains=keyword) | Q(full_address__icontains=keyword)).values()
#                 properties_list.append(properties)
                
#                 # Get device_name for each property
#                 for property in properties:
#                     devices = Device.objects.filter(property_id=property['id']).values('device_name')
#                     print(devices)
#                     property['devices'] = devices
                    
#             except Exception as e:
#                 return Response({'error': 'Invalid search parameter {e}'})
            
#         else:
#             properties = Property.objects.all().values()
#             properties_list.append(properties)
            
#             # Get device_name for each property
#             for property in properties:
#                 devices = Device.objects.filter(property_id=property['id']).values('device_name')
#                 property['devices'] = devices

#         return Response({'results': properties_list})

class Property_Search_location(APIView):
    def post(self, request):
        data = request.data
        keyword = data.get("keyword")

        properties_list = []
        
        if keyword:
            # Validate keyword length
            if len(keyword) < 3:
                return Response({'error': 'Keyword length must be at least 3 characters'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                properties = Property.objects.filter(Q(location__icontains=keyword) | Q(full_address__icontains=keyword)).values()
                properties_list.append(properties)
                
                # Get device_name for each property
                for property in properties:
                    devices = Device.objects.filter(property_id=property['id']).values('device_name')
                    property['devices'] = devices
                    
            except Exception as e:
                return Response({'error': f'Invalid search parameter: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            properties = Property.objects.all().values()

            properties_list.append(properties)
            
            # Get device_name for each property
            for property in properties:
                devices = Device.objects.filter(property_id=property['id']).values('device_name')
                if devices.exists():
                    property['devices'] = devices
                else:
                     property['devices']=[{"device_name": "No Device Found"}]

        return Response({'results': properties_list}, status=status.HTTP_200_OK)


