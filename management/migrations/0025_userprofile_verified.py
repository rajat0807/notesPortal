# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-03 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0024_auto_20170101_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]