# Generated by Django 2.2.2 on 2023-04-14 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evChargerApp', '0015_auto_20230414_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordatadetails',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
