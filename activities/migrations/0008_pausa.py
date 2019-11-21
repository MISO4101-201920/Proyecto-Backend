# Generated by Django 2.2.4 on 2019-11-21 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_merge_20191109_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pausa',
            fields=[
                ('actividad_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activities.Actividad')),
                ('enunciado', models.CharField(max_length=200)),
                ('tiempo', models.FloatField(default=0)),
            ],
            bases=('activities.actividad',),
        ),
    ]
