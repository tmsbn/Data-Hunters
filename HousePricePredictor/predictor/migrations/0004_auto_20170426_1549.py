# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0003_auto_20170424_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='housedata',
            name='id',
        ),
        migrations.AddField(
            model_name='housedata',
            name='no',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
