# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0049_auto_20150822_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='classes',
            field=models.ManyToManyField(default=0, related_name='school_questions', to='App.UserDefinedClass'),
        ),
    ]
