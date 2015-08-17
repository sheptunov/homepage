# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_auto_20150813_0852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='image',
        ),
        migrations.RemoveField(
            model_name='project',
            name='thumbnail',
        ),
        migrations.AddField(
            model_name='entity',
            name='project',
            field=models.ForeignKey(default='1', to='portfolio.Project'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entity',
            name='thumbnail',
            field=models.ImageField(upload_to=b'', null=True, verbose_name=b'Thumbnail', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='order',
            field=models.IntegerField(default=1, blank=True),
        ),
    ]
