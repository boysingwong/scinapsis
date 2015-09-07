# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scin', '0002_pub_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='pub_support_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section_id', models.IntegerField()),
                ('header', models.CharField(max_length=800)),
                ('content', models.TextField()),
                ('url', models.CharField(max_length=100)),
                ('doc_id', models.ForeignKey(to='scin.pub_meta')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='pub_meta',
            name='pdf_address',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pub_meta',
            name='src_address',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
