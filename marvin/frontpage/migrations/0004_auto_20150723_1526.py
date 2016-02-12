# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0003_auto_20150701_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='bayesConfidence',
            field=models.DecimalField(default='0.000', max_digits=4, decimal_places=3, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='app',
            name='bayesResult',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='status',
            field=models.CharField(default=b'QUEUED', max_length=20),
            preserve_default=True,
        ),
    ]
