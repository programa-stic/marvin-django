# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0009_app_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_metadata',
            name='author',
            field=models.CharField(max_length=80, blank=True),
            preserve_default=True,
        ),
    ]
