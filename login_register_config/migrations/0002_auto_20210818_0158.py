# Generated by Django 3.2.6 on 2021-08-18 01:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('login_register_config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginregisterconfig',
            name='type',
            field=models.CharField(max_length=32, verbose_name='登录注册配置类型'),
        ),
        migrations.AlterField(
            model_name='loginregisterconfig',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='唯一标识'),
        ),
    ]
