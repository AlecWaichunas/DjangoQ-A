# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0027_notifications_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
