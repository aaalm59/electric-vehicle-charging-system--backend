from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser,BaseUserManager, Group
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils import timezone


#from model_utils.models import TimeStampedModel


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
class User(AbstractUser):
    username = None
    email = models.EmailField(blank=True,unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    user_type = ((1, 'Super_Admin'), (2, "Consumer"), (3, 'Aviconn_Executive'),
                 (4, 'Customer'), (5, 'Property_Manager'),)
    UserType = models.PositiveIntegerField(default=1, choices=user_type)
    Contact_number = models.CharField(max_length=15, help_text='Enter the contact number')
    objects = UserManager()



def Create_Group(sender, instance, *args, **kwargs):
    if instance._state.adding is True and len(Group.objects.filter(name=instance.get_UserType_display())):
        print("Group has been created successfully ")
        Group.objects.create(name=instance.get_UserType_display())


def Add_group_to_user(sender, instance, *args, **kwargs):
    try:
        if instance.UserType == 1:
            User.objects.filter(username=instance.username).update(is_staff=True)
        g = Group.objects.filter(name=instance.get_UserType_display())
        print(g)
        print("Instance has been added inside the group")
        instance.groups.set(g)

    except Exception:
        pass


post_save.connect(Add_group_to_user, sender=User)
pre_save.connect(Create_Group, sender=User)

class OTP(models.Model):
    otp = models.CharField(blank=True, null=True, max_length=5)
    user_id = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return "OTP  {} on {}".format(self.otp, self.created)

    def __str__(self):
        return "OTP  {} on {}".format(self.otp, self.created)


class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    property_name = models.CharField(max_length=20,null=True, blank=True)
    full_address = models.CharField(max_length=30,null=True, blank=True)
    location = models.CharField(max_length=30,null=True, blank=True)
    total_no_of_devices = models.PositiveIntegerField(null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="manager")
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.property_name

class Image(models.Model):
    which_property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    image_file = models.FileField()
    image_id = models.CharField(max_length=10)

    def __str__(self):
        return self.image_file

    def __unicode__(self):
        return self.image_file



class Device(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    device_name = models.CharField(max_length=30, null=True, blank=True,unique=True)
    created = models.DateTimeField(auto_now=datetime.now(), blank=True, null=True)

    def __str__(self):
        return self.device_name


class Sockets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="device")
    SOCKETS = ((1, "Socket1"), (2, "Socket2"), (3, "Socket3"))
    socket = models.PositiveIntegerField(choices=SOCKETS)
    status = models.CharField(max_length=10, null=True, blank=True)
    pending_Command = models.CharField(max_length=10,null=True,blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.socket) + " " + str(self.device)


class SocketLiveData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    socket = models.ForeignKey(Sockets, on_delete=models.CASCADE)
    socket_Id = models.IntegerField(null=True,default=0,blank=True)
    url_field = models.URLField(max_length=200,null=True,blank=True,default=0)
    voltage = models.FloatField(null=True,default=0,blank=True)
    current = models.FloatField(null=True,blank=True,default=0)
    unit_consumption = models.FloatField(default=0,null=True,blank=True)
    # reading_from = models.DateTimeField(null=True, blank=True)
    # reading_to = models.DateTimeField(blank=True, null=True)
    total_time = models.IntegerField(blank=True,default=0, null = True)

    # def __str__(self):
        # return str(self.socket) + " " + str(self.device)

    


class DailyPropertyReading(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE,null=True,blank=True)
    socket = models.ForeignKey(Sockets, on_delete=models.CASCADE, null=True, blank=True)
    unit_consumption = models.FloatField(default=0)
    reading_for = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class ConsumerHistory(models.Model):
    consumer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    deviceId = models.CharField(max_length=25,null=True,blank=True)
    property = models.CharField(max_length=25,null=True,blank=True)
    location = models.CharField(max_length=25,null=True,blank=True)
    unit_consumed = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True,blank=True)


class SensorDataDetails(models.Model):
    deviced_id=models.CharField(max_length=10)
    from_time=models.DateTimeField(default=timezone.now())
    to_time=models.DateTimeField(default=timezone.now())
    status=models.BooleanField(default=False)
    is_on_count=models.IntegerField(null=True,blank=True)


    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.from_time = timezone.now()
    #         self.to_time = timezone.now()
    #     return super(SensorDataDetails, self).save(*args, **kwargs)

from django.db import models

class Sensor(models.Model):
    sensor_id = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # add any other relevant fields here

    def total_time(self):
        return self.end_time - self.start_time

class Wallet(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



