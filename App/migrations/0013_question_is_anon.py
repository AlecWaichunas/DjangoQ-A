# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0012_answer_is_anon'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_anon',
            field=models.BooleanField(default=False),
        ),
    ]
