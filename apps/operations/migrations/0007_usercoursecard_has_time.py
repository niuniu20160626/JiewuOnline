# Generated by Django 3.0.3 on 2020-04-25 05:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0006_usercoursecard'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercoursecard',
            name='has_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='课卡失效时间'),
        ),
    ]
