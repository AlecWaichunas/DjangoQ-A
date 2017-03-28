# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_auto_20150808_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='parent_class',
            field=models.ForeignKey(related_name='question_parent_class', default=0, to='App.UserDefinedClass'),
        ),
        migrations.AddField(
            model_name='userdefinedclass',
            name='school_name',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
