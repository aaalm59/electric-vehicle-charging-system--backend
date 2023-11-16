
from datetime import timedelta
from django.utils import timezone
from rest_framework import filters, serializers, viewsets

from .models import Sensor

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'