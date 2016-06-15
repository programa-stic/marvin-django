# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontpage', '0016_dynamictestresults_last_check'),
    ]

    operations = [
        migrations.CreateModel(
            name='App_comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contents', models.TextField()),
                ('app', models.ForeignKey(to='frontpage.App')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('vuln', models.ManyToManyField(to='frontpage.VulnerabilityResult')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
