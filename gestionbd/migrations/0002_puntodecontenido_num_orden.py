# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-13 06:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionbd', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntodecontenido',
            name='num_orden',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]