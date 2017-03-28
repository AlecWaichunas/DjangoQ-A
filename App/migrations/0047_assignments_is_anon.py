# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0046_userdefinedclass_assignments'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignments',
            name='is_anon',
            field=models.BooleanField(default=False),
        ),
    ]
