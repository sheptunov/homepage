# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_auto_20150810_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'', verbose_name=b'Image')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.CharField(default='1', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ForeignKey(to='portfolio.Entity'),
        ),
        migrations.AlterField(
            model_name='project',
            name='thumbnail',
            field=models.ImageField(upload_to=b'', null=True, verbose_name=b'Thumbnail', blank=True),
        ),
    ]
