# Generated by Django 5.1.2 on 2024-10-16 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_remove_estudiante_correo_remove_estudiante_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
