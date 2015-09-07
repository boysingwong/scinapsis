# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scin', '0003_auto_20150204_0007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pub_figure',
            old_name='doc_id',
            new_name='doc',
        ),
        migrations.RenameField(
            model_name='pub_material_n_method',
            old_name='doc_id',
            new_name='doc',
        ),
        migrations.RenameField(
            model_name='pub_result',
            old_name='doc_id',
            new_name='doc',
        ),
        migrations.RenameField(
            model_name='pub_support_info',
            old_name='doc_id',
            new_name='doc',
        ),
    ]
