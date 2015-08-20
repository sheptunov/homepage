# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0011_remove_entity_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='image',
        ),
        migrations.AddField(
            model_name='entity',
            name='image',
            field=models.ImageField(default='1', upload_to=b'', verbose_name=b'Image'),
            preserve_default=False,
        ),
    ]
