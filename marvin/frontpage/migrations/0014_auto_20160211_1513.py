# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0013_vulnerabilityresult_severity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ManagedButEmpty',
        ),
        migrations.DeleteModel(
            name='NoUpdatedField',
        ),
        migrations.DeleteModel(
            name='Unmanaged',
        ),
        migrations.AlterField(
            model_name='vulnerabilityresult',
            name='vuln_method',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
    ]
