# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-01 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0023_auto_20170101_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.FileField(default='default_pic.jpg', upload_to='profile_pictures'),
        ),
    ]
