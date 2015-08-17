# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0012_auto_20150813_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='title',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]
