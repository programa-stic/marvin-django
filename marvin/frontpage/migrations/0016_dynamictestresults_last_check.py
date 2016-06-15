# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0015_vulnerabilityresult_scheduledfordt'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamictestresults',
            name='last_check',
            field=models.DateField(default=datetime.datetime(2016, 4, 6, 14, 53, 30, 596196, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
