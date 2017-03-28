# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0055_passwordlink_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordlink',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='passwordlink',
            name='url',
            field=models.CharField(default=0, max_length=128),
        ),
    ]
