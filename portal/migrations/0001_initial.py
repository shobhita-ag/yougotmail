# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-24 14:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('email', models.CharField(max_length=254)),
                ('email_type', models.IntegerField(choices=[(1, 'to'), (2, 'cc'), (3, 'bcc')], default=1)),
                ('subject', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
