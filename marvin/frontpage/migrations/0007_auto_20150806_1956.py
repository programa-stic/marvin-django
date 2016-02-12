# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0006_auto_20150803_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vulnerabilityresult',
            name='dynamic_test_params',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
