# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='uploaded',
            field=models.DateField(default=datetime.datetime(2015, 6, 9, 19, 27, 8, 815694, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
