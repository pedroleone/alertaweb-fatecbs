# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 19:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0016_reportedalert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportedalert',
            name='alert_organ',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='alertas.Organ'),
        ),
    ]
