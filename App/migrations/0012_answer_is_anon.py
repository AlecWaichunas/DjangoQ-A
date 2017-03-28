# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_auto_20150808_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_anon',
            field=models.BooleanField(default=False),
        ),
    ]
