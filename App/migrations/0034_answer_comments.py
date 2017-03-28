# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0033_userdefinedclass_discussions'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='comments',
            field=models.ManyToManyField(default=0, related_name='answer_comments', to='App.Comments'),
        ),
    ]
