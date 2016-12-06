# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 13:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0004_auto_20161203_0827'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idcard',
            old_name='open_id',
            new_name='open_id_found',
        ),
        migrations.AddField(
            model_name='idcard',
            name='end_time',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='idcard',
            name='open_id_lost',
            field=models.CharField(db_index=True, default=0, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='idcard',
            name='status',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='idcard',
            name='id_num',
            field=models.CharField(db_index=True, max_length=64),
        ),
    ]
