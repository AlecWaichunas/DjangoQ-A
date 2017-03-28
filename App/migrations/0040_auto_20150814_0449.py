# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0039_auto_20150814_0148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussion',
            name='points',
        ),
        migrations.RemoveField(
            model_name='replies',
            name='points',
        ),
    ]
