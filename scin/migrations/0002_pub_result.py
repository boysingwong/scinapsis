# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='pub_result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section_id', models.IntegerField()),
                ('header', models.CharField(max_length=800)),
                ('content_seq', models.IntegerField()),
                ('content', models.TextField()),
                ('doc_id', models.ForeignKey(to='scin.pub_meta')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
