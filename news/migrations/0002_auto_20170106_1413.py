# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-06 14:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-updated']},
        ),
    ]
