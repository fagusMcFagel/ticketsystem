# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-04 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20170905_1153'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolvingMeasures',
            fields=[
                ('measureid', models.AutoField(primary_key=True, serialize=False, verbose_name='TicketID')),
                ('ticketid', models.IntegerField(verbose_name='TicketID')),
                ('creationdatetime', models.DateTimeField(verbose_name='Zeitpunkt')),
                ('shortdsc', models.CharField(max_length=100, verbose_name='Kurzbeschreibung')),
                ('dsc', models.CharField(blank=True, max_length=400, verbose_name='Beschreibung')),
                ('result', models.CharField(max_length=400, verbose_name='Ergebnis')),
                ('isSolution', models.CharField(choices=[('', ''), ('temporary', 'temporär'), ('partly', 'teilweise'), ('solution', 'Lösung')], max_length=30, verbose_name='Ist Lösung')),
            ],
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='solution',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='category',
            field=models.CharField(choices=[('Problem', 'Problem'), ('Vorschlag', 'Vorschlag')], max_length=30, verbose_name='Art'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('', ''), ('low', 'niedrig'), ('moderate', 'normal'), ('high', 'hoch')], max_length=20, verbose_name='Priorität'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('open', 'Offen'), ('delayed', 'Verzögert'), ('processing', 'In Bearbeitung')], max_length=20, verbose_name='Status'),
        ),
    ]
