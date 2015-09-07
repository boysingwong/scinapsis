# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scin', '0004_auto_20150315_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='pub_meta',
            name='citation',
            field=models.CharField(max_length=800, null=True),
            preserve_default=True,
        ),
    ]
