# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0051_question_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignments',
            name='details',
            field=models.CharField(default=0, max_length=2000),
        ),
    ]
