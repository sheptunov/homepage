# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(help_text=b'Author', max_length=255)),
                ('email', models.EmailField(help_text=b'Email', max_length=254, null=True, blank=True)),
                ('message', models.CharField(help_text=b'Message', max_length=255)),
                ('date_created', models.DateTimeField(help_text=b'Creation Date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Title', max_length=100, blank=True)),
                ('cover', models.ImageField(upload_to=b'', verbose_name=b'Cover')),
                ('date_created', models.DateTimeField(help_text=b'Creation Date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
    ]
