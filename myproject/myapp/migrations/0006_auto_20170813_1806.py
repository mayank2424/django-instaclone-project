# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 12:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20170813_1738'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='Full_name',
            new_name='name',
        ),
    ]
