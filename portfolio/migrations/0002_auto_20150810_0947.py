# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='cover',
        ),
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.ImageField(default='temp', upload_to=b'', verbose_name=b'Image'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='thumbnail',
            field=models.ImageField(upload_to=b'', verbose_name=b'Thumbnail', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(help_text=b'Title', max_length=100),
        ),
    ]
