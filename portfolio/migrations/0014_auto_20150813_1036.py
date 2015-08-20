# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0013_auto_20150813_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='gallery',
            field=models.ForeignKey(verbose_name=b'+', to='portfolio.Project'),
        ),
    ]
