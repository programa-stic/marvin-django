# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0004_auto_20150723_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vulnerabilityresult',
            name='confidence',
            field=models.CharField(max_length=10, blank=True),
            preserve_default=True,
        ),
    ]
