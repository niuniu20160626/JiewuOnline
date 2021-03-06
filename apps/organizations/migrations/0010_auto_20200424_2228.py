# Generated by Django 3.0.3 on 2020-04-24 22:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0009_notic'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('card_type', models.CharField(choices=[('ck', '次卡'), ('tk', '通卡'), ('sk', '一对一课卡')], default='ck', max_length=4, verbose_name='课卡类型')),
                ('name', models.CharField(max_length=25, verbose_name='课卡名称')),
                ('nums', models.IntegerField(default=0, verbose_name='次数')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='课卡价格')),
                ('has_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='有效期')),
                ('desc', models.CharField(max_length=100, verbose_name='备注说明')),
                ('image', models.ImageField(upload_to='org/coursecard/%Y/%m', verbose_name='封面')),
            ],
            options={
                'verbose_name': '课卡',
                'verbose_name_plural': '课卡',
            },
        ),
        migrations.AlterModelOptions(
            name='notic',
            options={'verbose_name': '网站公告', 'verbose_name_plural': '网站公告'},
        ),
        migrations.AlterField(
            model_name='notic',
            name='title',
            field=models.CharField(max_length=25, verbose_name='公告标题'),
        ),
    ]
