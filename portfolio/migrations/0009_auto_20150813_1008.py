# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_entity_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entity',
            name='project',
        ),
        migrations.AddField(
            model_name='entity',
            name='order',
            field=models.IntegerField(default=1, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.ImageField(default=1, upload_to=b'', verbose_name=b'Image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entity',
            name='image',
            field=models.ForeignKey(to='portfolio.Project'),
        ),
    ]
