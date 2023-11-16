# Generated by Django 2.2.2 on 2023-04-17 11:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evChargerApp', '0019_auto_20230417_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='sensordatadetails',
            name='from_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 17, 11, 41, 48, 619219)),
        ),
        migrations.AlterField(
            model_name='sensordatadetails',
            name='to_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 17, 11, 41, 48, 619371)),
        ),
    ]