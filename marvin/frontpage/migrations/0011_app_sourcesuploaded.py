# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0010_auto_20151016_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='sourcesUploaded',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
