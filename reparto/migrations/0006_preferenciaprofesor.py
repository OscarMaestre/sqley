# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-23 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionbd', '0007_competenciageneral'),
        ('reparto', '0005_auto_20170423_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreferenciaProfesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reparto.ModuloEnReparto')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionbd.Profesor')),
            ],
        ),
    ]