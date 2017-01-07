# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-31 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0020_auto_20161231_0945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=models.FileField(blank=True, upload_to='profile_pictures'),
        ),
    ]
