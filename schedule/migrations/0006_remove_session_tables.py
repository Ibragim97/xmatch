# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 18:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20170806_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='tables',
        ),
    ]
