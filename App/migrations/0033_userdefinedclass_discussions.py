# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0032_auto_20150813_0503'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdefinedclass',
            name='discussions',
            field=models.ManyToManyField(default=0, related_name='userdefinedclass_discussions', to='App.Discussion'),
        ),
    ]
