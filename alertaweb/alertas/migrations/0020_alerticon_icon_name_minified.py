# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-02 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0019_auto_20160216_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerticon',
            name='icon_name_minified',
            field=models.CharField(max_length=100, null=True, verbose_name='nome do ícone pequeno'),
        ),
    ]
