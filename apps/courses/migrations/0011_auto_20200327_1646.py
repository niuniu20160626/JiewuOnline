# Generated by Django 3.0.3 on 2020-03-27 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20200322_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='apoint_nums',
            field=models.IntegerField(default=0, verbose_name='预约人数'),
        ),
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='预约人数'),
        ),
    ]
