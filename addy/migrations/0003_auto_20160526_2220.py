# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-26 16:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addy', '0002_auto_20160526_2219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachments',
            name='user',
        ),
        migrations.DeleteModel(
            name='Attachments',
        ),
    ]
