# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-03 12:59
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0007_auto_20170903_1113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumno',
            name='id',
        ),
        migrations.AlterField(
            model_name='alumno',
            name='dni',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='En el DNI/NIE por favor, usa solo numeros y mayúsculas. Ni guiones, ni puntos ni cualquier otro símbolo, gracias', regex='([0-9]{7,8}[A-Z])|([A-Z][0-9]{7,8})')]),
        ),
    ]