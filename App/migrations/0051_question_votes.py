# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0050_auto_20150822_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='votes',
            field=models.ManyToManyField(default=0, related_name='question_votes', to='App.QVote'),
        ),
    ]
