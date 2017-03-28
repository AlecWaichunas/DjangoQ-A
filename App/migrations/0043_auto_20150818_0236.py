# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0042_auto_20150818_0230'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdefinedclass',
            name='code',
            field=models.CharField(default=0, max_length=9),
        ),
        migrations.AlterField(
            model_name='userdefinedclass',
            name='school_name',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
