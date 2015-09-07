# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scin', '0008_pub_abstract_pub_discussion'),
    ]

    operations = [
        migrations.AddField(
            model_name='pub_abstract',
            name='content_seq',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pub_abstract',
            name='header',
            field=models.CharField(max_length=800, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pub_abstract',
            name='section_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
