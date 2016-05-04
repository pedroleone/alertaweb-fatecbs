# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 15:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0011_announcement'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon_name', models.CharField(max_length=100, verbose_name='nome do ícone')),
                ('icon_url', models.CharField(max_length=200, verbose_name='url da imagem do ícone')),
            ],
        ),
        migrations.AddField(
            model_name='alerttype',
            name='alert_icon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='alertas.AlertIcon', verbose_name='cor'),
        ),
    ]
