# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-15 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_customapps_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='insight',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
