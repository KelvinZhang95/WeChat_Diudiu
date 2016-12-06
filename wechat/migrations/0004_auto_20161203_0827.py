# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-03 08:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0003_auto_20161203_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='idcard',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='others',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
