# Generated by Django 3.0.3 on 2020-03-28 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0002_userorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='istype',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userorder',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
    ]