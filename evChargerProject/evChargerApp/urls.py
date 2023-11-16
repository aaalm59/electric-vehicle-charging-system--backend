
from django.urls import path, include

from evChargerProject.evChargerApp import views
from .views import *
from .tests import *
#from rest_framework import routers
# from django.urls import path
# from .views import PaymentView, payment_callback
#router = routers.DefaultRouter()
#router.register('tokens', TokenViewSet)

urlpatterns = [

    #path('', include(router.urls)),
    path('login/', LoginApi.as_view()),
    path('registerUser/', RegisterData.as_view()),
    path('validateToken/', ValidatedToken.as_view()),
    path('fetchProperties/', FetchProperties.as_view()),
    path('createProperty/', CreateProperty.as_view()),
    path('addManager/', CreateManager.as_view()),
    path('addDevice/', AddDevice.as_view()),
    path('fetchDevices/',  FetchDevice.as_view()),
    path('savingMonthlyTrend/',EnergyMonthyTrendApi.as_view()),
    path('deviceMonthlyConsumptionData/', EnergySavingMonthlyBarChart.as_view()),
    path('liveDataApi/',LiveDataApi.as_view()),
    path('consumerHistoryApi/', ConsumerHistoryApi.as_view()),
    # path('consumerBillApi/',ConsumerBillApi.as_view()),
    path('fetchConsumerSelectedDeviceInfo/', FetchConsumerSelectedDeviceInfo.as_view()),
    path('socketOnApi/',SocketOnApi.as_view()),
    path('socketOffApi/',SocketOffApi.as_view()),
    path('dummyAPi/', dummyAPi.as_view()),
    path('checkSocketUsedByUser/', CheckSocketUsedByUser.as_view()),
    path('property/search/location/', Property_Search_location.as_view()),
    path('payment/', PaymentView.as_view()),
    path('payments/', Start_payment.as_view()),
    path('payment/callback/', payment_callback),

]

