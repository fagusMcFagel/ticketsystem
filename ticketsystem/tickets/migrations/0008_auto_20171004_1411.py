# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-04 12:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_auto_20171004_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='sector',
            field=models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]