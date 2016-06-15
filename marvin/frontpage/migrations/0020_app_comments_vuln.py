# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0019_remove_app_comments_vuln'),
    ]

    operations = [
        migrations.AddField(
            model_name='app_comments',
            name='vuln',
            field=models.ForeignKey(to='frontpage.VulnerabilityResult', null=True),
            preserve_default=True,
        ),
    ]
