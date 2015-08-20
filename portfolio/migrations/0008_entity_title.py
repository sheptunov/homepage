# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_auto_20150813_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='title',
            field=models.CharField(default='1', max_length=500),
            preserve_default=False,
        ),
    ]
