# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-04 12:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0006_auto_20171004_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solvingmeasures',
            name='ticket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.Ticket', verbose_name='Ticket'),
        ),
    ]