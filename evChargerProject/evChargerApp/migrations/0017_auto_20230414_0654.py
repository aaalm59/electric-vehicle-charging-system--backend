# Generated by Django 2.2.2 on 2023-04-14 06:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('evChargerApp', '0016_auto_20230414_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordatadetails',
            name='from_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sensordatadetails',
            name='to_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 14, 6, 54, 1, 394697, tzinfo=utc)),
        ),
    ]
