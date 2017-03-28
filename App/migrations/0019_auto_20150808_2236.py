# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0018_auto_20150808_2132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='viewer',
            old_name='answer',
            new_name='question',
        ),
        migrations.RemoveField(
            model_name='viewer',
            name='user',
        ),
        migrations.AddField(
            model_name='viewer',
            name='ip',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AddField(
            model_name='viewer',
            name='session',
            field=models.CharField(default=0, max_length=40),
        ),
    ]
