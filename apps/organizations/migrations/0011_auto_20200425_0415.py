# Generated by Django 3.0.3 on 2020-04-25 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0010_auto_20200424_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecard',
            name='desc',
            field=models.CharField(default='课卡的有效期从购买时开始算起', max_length=100, verbose_name='备注说明'),
        ),
        migrations.AlterField(
            model_name='coursecard',
            name='nums',
            field=models.IntegerField(default=2147483647, verbose_name='次数'),
        ),
    ]
