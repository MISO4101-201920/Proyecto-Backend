# Generated by Django 2.2.4 on 2019-11-09 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_auto_20191027_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='retroalimentacion',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='opcionmultiple',
            name='preguntaSeleccionMultiple',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opciones', to='activities.PreguntaOpcionMultiple'),
        ),
    ]