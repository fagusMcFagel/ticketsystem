# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_auto_20170810_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]