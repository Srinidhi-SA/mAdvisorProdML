# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-14 10:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_insight_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, null=True)),
                ('slug', models.SlugField(blank=True)),
                ('column_data_raw', models.TextField(default='{}')),
                ('app_id', models.IntegerField(default=0, null=True)),
                ('data', models.TextField(default='{}')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('bookmarked', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Dataset')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Job')),
            ],
            options={
                'ordering': ['-created_on', '-updated_on'],
            },
        ),
    ]