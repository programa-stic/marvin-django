# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0020_app_comments_vuln'),
    ]

    operations = [
        migrations.CreateModel(
            name='Java_Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('package_name', models.CharField(max_length=300)),
                ('app', models.ManyToManyField(to='frontpage.App')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
