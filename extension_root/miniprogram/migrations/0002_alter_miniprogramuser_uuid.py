# Generated by Django 3.2.6 on 2021-08-18 01:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('miniprogram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miniprogramuser',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='唯一标识'),
        ),
    ]
