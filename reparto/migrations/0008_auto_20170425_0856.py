# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-25 08:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reparto', '0007_preferenciaprofesor_prioridad'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='preferenciaprofesor',
            options={'ordering': ['modulo']},
        ),
    ]