# Generated by Django 2.2.2 on 2023-04-14 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evChargerApp', '0008_auto_20230328_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorDataDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviced_id', models.CharField(max_length=10)),
                ('from_time', models.DateTimeField(auto_now=True)),
                ('to_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField()),
                ('is_on_count', models.IntegerField()),
            ],
        ),
    ]
