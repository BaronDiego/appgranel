# Generated by Django 3.2.6 on 2021-08-27 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actividad',
            options={'ordering': ['creado']},
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='um',
            field=models.IntegerField(blank=True, null=True, verbose_name='Usuario que modifica'),
        ),
    ]
