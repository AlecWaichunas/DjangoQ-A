# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0041_remove_viewer_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdefinedclass',
            name='school_name',
            field=models.CharField(default=0, max_length=9),
        ),
    ]
