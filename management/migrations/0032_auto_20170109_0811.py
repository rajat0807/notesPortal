# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-09 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0031_auto_20170109_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.chapters'),
        ),
    ]
