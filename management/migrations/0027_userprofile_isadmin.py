# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-04 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0026_auto_20170103_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='isAdmin',
            field=models.BooleanField(default=False),
        ),
    ]