# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0040_auto_20150814_0449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viewer',
            name='session',
        ),
    ]
