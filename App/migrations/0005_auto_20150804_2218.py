# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_auto_20150804_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='classes',
            field=models.ManyToManyField(default=0, related_name='userprofile_classes', to='App.UserDefinedClass'),
        ),
    ]
