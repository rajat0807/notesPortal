# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-17 05:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0033_userprofile_tobedeleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='toBeDeleted',
        ),
    ]