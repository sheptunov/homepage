# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0016_project_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500, blank=True)),
                ('image', models.ImageField(upload_to=b'', verbose_name=b'Image')),
                ('thumbnail', models.ImageField(upload_to=b'', null=True, verbose_name=b'Thumbnail', blank=True)),
                ('order', models.IntegerField(default=1, blank=True)),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.RemoveField(
            model_name='entity',
            name='gallery',
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(max_length=30, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='Entity',
        ),
        migrations.AddField(
            model_name='image',
            name='gallery',
            field=models.ForeignKey(verbose_name=b'+', to='portfolio.Project'),
        ),
    ]
