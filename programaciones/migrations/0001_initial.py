# Generated by Django 3.0.4 on 2020-07-18 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestionbd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calificador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=180)),
            ],
            options={
                'verbose_name_plural': 'Calificadores',
                'db_table': 'calificadores',
            },
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Evaluaciones',
                'db_table': 'evaluaciones',
            },
        ),
        migrations.CreateModel(
            name='InstrumentoEvaluacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Instrumentos de evaluacion',
                'db_table': 'instrumentos_evaluacion',
            },
        ),
        migrations.CreateModel(
            name='Interviene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('es_criterio_minimo', models.BooleanField()),
                ('ponderacion', models.IntegerField()),
                ('calificador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programaciones.Calificador')),
                ('criterio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionbd.CriterioDeEvaluacion')),
            ],
            options={
                'verbose_name_plural': 'Criterios en UT',
                'db_table': 'criterios_unidades_trabajo',
            },
        ),
        migrations.CreateModel(
            name='Programacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=240)),
                ('modulo', models.ManyToManyField(to='gestionbd.Modulo')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionbd.Profesor')),
            ],
            options={
                'verbose_name_plural': 'Programaciones',
                'db_table': 'programaciones',
            },
        ),
        migrations.CreateModel(
            name='PuntoMetodologico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=4096)),
            ],
            options={
                'verbose_name_plural': 'Puntos de Metodologia',
                'db_table': 'puntos_de_metodologia',
            },
        ),
        migrations.CreateModel(
            name='RecursoDidactico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Recursos didacticos',
                'db_table': 'recursos_didacticos',
            },
        ),
        migrations.CreateModel(
            name='UnidadDeTrabajo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('nombre', models.CharField(max_length=180)),
                ('sesiones', models.IntegerField()),
                ('contenidos', models.ManyToManyField(to='gestionbd.Contenido')),
                ('criterios', models.ManyToManyField(through='programaciones.Interviene', to='gestionbd.CriterioDeEvaluacion')),
                ('evaluaciones', models.ManyToManyField(to='programaciones.Evaluacion')),
                ('instrumentos', models.ManyToManyField(to='programaciones.InstrumentoEvaluacion')),
                ('programacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programaciones.Programacion')),
                ('puntos_contenido', models.ManyToManyField(to='gestionbd.PuntoDeContenido')),
                ('puntos_metodologia', models.ManyToManyField(to='programaciones.PuntoMetodologico')),
                ('recursos', models.ManyToManyField(to='programaciones.RecursoDidactico')),
                ('resultado_aprendizaje', models.ManyToManyField(to='gestionbd.ResultadoDeAprendizaje')),
            ],
            options={
                'verbose_name_plural': 'Unidades de Trabajo',
                'db_table': 'unidades_de_trabajo',
            },
        ),
        migrations.CreateModel(
            name='ObjetivosModulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionbd.Modulo')),
                ('objetivos', models.ManyToManyField(to='gestionbd.ObjetivoGeneral')),
            ],
            options={
                'verbose_name_plural': 'Objetivos de modulo',
                'db_table': 'objetivosmodulo',
            },
        ),
        migrations.AddField(
            model_name='interviene',
            name='unidad_de_trabajo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programaciones.UnidadDeTrabajo'),
        ),
        migrations.CreateModel(
            name='CompetenciasModulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competencias', models.ManyToManyField(to='gestionbd.Competencia')),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionbd.Modulo')),
            ],
            options={
                'verbose_name_plural': 'Competencias del modulo',
                'db_table': 'competenciasmodulo',
            },
        ),
    ]
