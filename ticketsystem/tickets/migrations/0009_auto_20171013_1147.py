# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-13 09:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_auto_20171004_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measures',
            fields=[
                ('measureid', models.AutoField(primary_key=True, serialize=False, verbose_name='UID')),
                ('creationdatetime', models.DateTimeField(verbose_name='Zeitpunkt')),
                ('shortdsc', models.CharField(max_length=100, verbose_name='Kurzbeschreibung')),
                ('dsc', models.CharField(max_length=400, null=True, verbose_name='Beschreibung')),
                ('result', models.CharField(max_length=400, verbose_name='Ergebnis')),
                ('isSolution', models.CharField(choices=[('', ''), ('unsuccesful', 'erfolglos'), ('temporary', 'temporär'), ('partly', 'teilweise'), ('solution', 'Lösung')], max_length=30, verbose_name='Ist Lösung')),
            ],
        ),
        migrations.RemoveField(
            model_name='solvingmeasures',
            name='ticket',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='responsible_person',
            field=models.ForeignKey(max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='sector',
            field=models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='auth.Group'),
        ),
        migrations.DeleteModel(
            name='SolvingMeasures',
        ),
        migrations.AddField(
            model_name='measures',
            name='ticket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Measures', to='tickets.Ticket'),
        ),
    ]
