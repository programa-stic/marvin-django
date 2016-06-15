# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0007_auto_20150806_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vulnerabilityresult',
            name='confidence',
            field=models.CharField(max_length=10, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vulnerabilityresult',
            name='dynamic_test_params',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
