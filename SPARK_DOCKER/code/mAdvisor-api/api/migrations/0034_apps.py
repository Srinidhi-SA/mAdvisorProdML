# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-30 09:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0033_stockdataset_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.IntegerField()),
                ('name', models.CharField(default='App', max_length=300)),
                ('slug', models.SlugField(blank=True, max_length=300)),
                ('displayName', models.CharField(default='App', max_length=300, null=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('tags', models.CharField(max_length=500, null=True)),
                ('iconName', models.CharField(max_length=300, null=True)),
                ('app_url', models.CharField(max_length=300, null=True)),
                ('status', models.CharField(default='Inactive', max_length=100, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['app_id'],
            },
        ),
    ]
