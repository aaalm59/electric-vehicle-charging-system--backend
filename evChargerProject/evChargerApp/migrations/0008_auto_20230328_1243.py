# Generated by Django 2.2.2 on 2023-03-28 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evChargerApp', '0007_socketlivedata_socket_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socketlivedata',
            name='current',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='socketlivedata',
            name='socket_Id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='socketlivedata',
            name='total_time',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='socketlivedata',
            name='url_field',
            field=models.URLField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='socketlivedata',
            name='voltage',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
