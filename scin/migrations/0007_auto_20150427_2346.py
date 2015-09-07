# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scin', '0006_auto_20150421_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='pub_figure',
            name='thumbnail',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pub_figure',
            name='url',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
