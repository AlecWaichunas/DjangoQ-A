# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0015_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdefinedclass',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
