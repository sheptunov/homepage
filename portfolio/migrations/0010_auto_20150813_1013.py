# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0009_auto_20150813_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='gallery',
            field=models.ForeignKey(default='1', to='portfolio.Project'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entity',
            name='image',
            field=models.ImageField(upload_to=b'', null=True, verbose_name=b'Image', blank=True),
        ),
    ]
