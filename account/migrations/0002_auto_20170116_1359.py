# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-16 13:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='title',
            new_name='fullname',
        ),
    ]
