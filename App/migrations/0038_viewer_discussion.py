# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0037_auto_20150813_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewer',
            name='discussion',
            field=models.ForeignKey(related_name='viewer_discussion', default=0, to='App.Discussion'),
        ),
    ]
