# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-09 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionbd', '0002_remove_cualificacionprofesional_completa'),
    ]

    operations = [
        migrations.CreateModel(
            name='EspecialidadProfesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad', models.CharField(choices=[('PS', 'Prof. Secundaria'), ('PT', 'Prof. Tecnico')], max_length=30)),
            ],
        ),
    ]