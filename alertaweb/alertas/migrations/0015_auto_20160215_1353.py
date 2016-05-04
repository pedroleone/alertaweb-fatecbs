# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 15:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0014_auto_20160215_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertcolor',
            name='alert_icon',
        ),
        migrations.AddField(
            model_name='alerttype',
            name='alert_icon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='alertas.AlertIcon', verbose_name='icon'),
        ),
    ]