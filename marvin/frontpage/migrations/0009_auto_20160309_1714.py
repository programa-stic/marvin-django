# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0009_app_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='DAstatus',
            field=models.CharField(default=b'N/A', max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='DCstatus',
            field=models.CharField(default=b'N/A', max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='DLstatus',
            field=models.CharField(default=b'QUEUED', max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='SAstatus',
            field=models.CharField(default=b'N/A', max_length=20),
            preserve_default=True,
        ),
    ]
