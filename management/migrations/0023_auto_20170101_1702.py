# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-01 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0022_auto_20161231_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.FileField(default='one.jpg', upload_to='profile_pictures'),
        ),
    ]
