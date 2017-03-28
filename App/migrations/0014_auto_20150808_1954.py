# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_question_is_anon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answerer',
            field=models.ForeignKey(default=0, to='App.UserProfile'),
        ),
    ]
