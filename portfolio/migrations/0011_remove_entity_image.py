# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0010_auto_20150813_1013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entity',
            name='image',
        ),
    ]
