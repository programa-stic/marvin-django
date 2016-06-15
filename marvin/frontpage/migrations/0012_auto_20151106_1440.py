# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0011_app_sourcesuploaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='vulnerabilityresult',
            name='vuln_class',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vulnerabilityresult',
            name='vuln_method',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
