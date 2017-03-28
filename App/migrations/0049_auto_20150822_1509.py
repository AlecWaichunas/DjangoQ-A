# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0048_auto_20150822_0127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='school',
            old_name='name',
            new_name='school_name',
        ),
    ]
