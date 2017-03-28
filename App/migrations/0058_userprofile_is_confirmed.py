# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0057_confirmlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
