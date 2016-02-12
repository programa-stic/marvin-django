# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0005_auto_20150724_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='bayesConfidence',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=3, blank=True),
            preserve_default=True,
        ),
    ]
