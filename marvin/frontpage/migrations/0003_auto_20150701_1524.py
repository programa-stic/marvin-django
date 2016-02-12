# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0002_app_uploaded'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('app', models.ForeignKey(to='frontpage.App')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='app',
            name='minSDK',
            field=models.CharField(default=' ', max_length=10, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='app',
            name='targetSDK',
            field=models.CharField(default=' ', max_length=10, blank=True),
            preserve_default=False,
        ),
    ]
