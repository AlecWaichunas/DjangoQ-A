# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0059_auto_20150903_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdefinedclass',
            name='member_count',
            field=models.IntegerField(default=0),
        ),
    ]
