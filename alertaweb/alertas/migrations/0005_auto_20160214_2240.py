# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 00:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0004_auto_20160214_2230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alertstatus',
            options={'ordering': ['status_code']},
        ),
    ]
