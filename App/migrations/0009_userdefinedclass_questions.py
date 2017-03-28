# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_auto_20150808_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdefinedclass',
            name='questions',
            field=models.ManyToManyField(default=0, related_name='userdefinedclass_questions', to='App.Question'),
        ),
    ]
