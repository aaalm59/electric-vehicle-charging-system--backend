# Generated by Django 2.2.2 on 2023-04-14 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evChargerApp', '0014_auto_20230414_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordatadetails',
            name='is_on_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sensordatadetails',
            name='status',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
