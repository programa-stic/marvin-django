# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0008_auto_20150806_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='App_metadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(db_index=True, max_length=100, blank=True)),
                ('version_string', models.CharField(max_length=30, blank=True)),
                ('author', models.CharField(max_length=40, blank=True)),
                ('date_upload', models.CharField(max_length=20, blank=True)),
                ('description', models.TextField()),
                ('app', models.ForeignKey(to='frontpage.App')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
