# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0038_viewer_discussion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discussion',
            old_name='poster',
            new_name='creator',
        ),
    ]
