# Generated by Django 2.2.2 on 2022-09-20 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import evChargerProject.evChargerApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('UserType', models.PositiveIntegerField(choices=[(1, 'Super_Admin'), (2, 'Consumer'), (3, 'Aviconn_Executive'), (4, 'Customer'), (5, 'Property_Manager')], default=1)),
                ('Contact_number', models.CharField(help_text='Enter the contact number', max_length=15)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', evChargerProject.evChargerApp.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(blank=True, max_length=5, null=True)),
                ('user_id', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sockets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('socket', models.PositiveIntegerField(choices=[(1, 'Socket1'), (2, 'Socket2'), (3, 'Socket3')])),
                ('is_active', models.BooleanField(default=False)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device', to='evChargerApp.Device')),
            ],
        ),
        migrations.CreateModel(
            name='SocketLiveData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voltage', models.FloatField(blank=True, null=True)),
                ('current', models.FloatField(blank=True, null=True)),
                ('unit_consumption', models.FloatField(blank=True, default=0, null=True)),
                ('reading_from', models.DateTimeField(blank=True, null=True)),
                ('reading_to', models.DateTimeField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evChargerApp.Device')),
                ('socket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evChargerApp.Sockets')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name', models.CharField(blank=True, max_length=20, null=True)),
                ('full_address', models.CharField(blank=True, max_length=30, null=True)),
                ('location', models.CharField(blank=True, max_length=30, null=True)),
                ('total_no_of_devices', models.PositiveIntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.FileField(upload_to='')),
                ('image_id', models.CharField(max_length=10)),
                ('which_property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evChargerApp.Property')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evChargerApp.Property'),
        ),
        migrations.CreateModel(
            name='DailyPropertyReading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_consumption', models.FloatField(default=0)),
                ('reading_for', models.DateTimeField(blank=True, null=True)),
                ('property_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evChargerApp.Property')),
                ('socket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evChargerApp.Sockets')),
                ('socketliveData', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evChargerApp.SocketLiveData')),
            ],
        ),
        migrations.CreateModel(
            name='ConsumerHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_consumed', models.FloatField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evChargerApp.Property')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]