# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scin', '0005_pub_meta_citation'),
    ]

    operations = [
        migrations.AddField(
            model_name='pub_meta',
            name='author',
            field=models.CharField(max_length=800, null=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='pub_meta',
			old_name='citation',
            new_name='citation_str',
        ),
        migrations.AddField(
            model_name='pub_meta',
            name='saves',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pub_meta',
            name='shares',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pub_meta',
            name='views',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
		migrations.AddField(
            model_name='pub_meta',
            name='citation',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
