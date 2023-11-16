# Generated by Django 2.2.2 on 2023-04-17 12:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evChargerApp', '0021_auto_20230417_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_id', models.CharField(max_length=50)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Sensor_d',
        ),
        migrations.AlterField(
            model_name='sensordatadetails',
            name='from_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 17, 12, 30, 32, 982332)),
        ),
        migrations.AlterField(
            model_name='sensordatadetails',
            name='to_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 17, 12, 30, 32, 982491)),
        ),
    ]
