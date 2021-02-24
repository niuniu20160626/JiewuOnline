# Generated by Django 3.0.3 on 2020-04-24 00:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0008_jchf_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operations', '0003_auto_20200328_1834'),
    ]

    operations = [
        migrations.CreateModel(
            name='JchfComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('comments', models.CharField(max_length=200, verbose_name='评论内容')),
                ('jchf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Jchf', verbose_name='精彩回放')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '精彩回放评论',
                'verbose_name_plural': '精彩回放评论',
            },
        ),
    ]
