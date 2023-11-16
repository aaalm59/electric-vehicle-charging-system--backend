
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *

admin.site.register(User),
admin.site.register(OTP),
admin.site.register(Property),
admin.site.register(Device),
admin.site.register(DailyPropertyReading),
admin.site.register(Sockets),
admin.site.register(SocketLiveData),
admin.site.register(ConsumerHistory)
admin.site.register(SensorDataDetails)
admin.site.register(Sensor)
admin.site.register(Wallet)



