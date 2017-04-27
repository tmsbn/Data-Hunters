# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 15:16
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0006_auto_20170427_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housedata',
            name='land_value',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000000), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='housedata',
            name='neighborhood',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000000), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='housedata',
            name='square_footage',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000000), django.core.validators.MinValueValidator(0)]),
        ),
    ]
