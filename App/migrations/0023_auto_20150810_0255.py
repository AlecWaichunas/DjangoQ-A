# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0022_auto_20150809_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdefinedclass',
            name='description',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='userdefinedclass',
            name='name',
            field=models.CharField(max_length=60),
        ),
    ]
