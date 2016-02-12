# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0007_auto_20150806_1956'),
    ]

    operations = [
        migrations.CreateModel(
            name='App_metadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(db_index=True, max_length=100, blank=True)),
                ('version_string', models.CharField(max_length=30, blank=True)),
                ('author', models.CharField(max_length=80, blank=True)),
                ('date_upload', models.CharField(max_length=20, blank=True)),
                ('description', models.TextField()),
                ('app', models.ForeignKey(to='frontpage.App')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='app',
            name='sourcesUploaded',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vulnerabilityresult',
            name='severity',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vulnerabilityresult',
            name='vuln_class',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vulnerabilityresult',
            name='vuln_method',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vulnerabilityresult',
            name='confidence',
            field=models.CharField(max_length=10, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vulnerabilityresult',
            name='dynamic_test_params',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
