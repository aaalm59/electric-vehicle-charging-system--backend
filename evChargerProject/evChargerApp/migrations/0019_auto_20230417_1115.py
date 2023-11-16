# Generated by Django 2.2.2 on 2023-04-17 11:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evChargerApp', '0018_auto_20230414_0657'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_id', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='sensordatadetails',
            name='from_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 17, 11, 15, 39, 711719)),
        ),
        migrations.AlterField(
            model_name='sensordatadetails',
            name='to_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 17, 11, 15, 39, 711866)),
        ),
    ]
