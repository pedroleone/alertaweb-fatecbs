# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0006_alert_alertapproval_alertdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
