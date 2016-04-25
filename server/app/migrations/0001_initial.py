# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 16:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predicate', models.CharField(blank=True, max_length=200)),
                ('criteria', models.CharField(max_length=200)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Node')),
            ],
        ),
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=1000)),
                ('root_node', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Node')),
            ],
        ),
    ]
