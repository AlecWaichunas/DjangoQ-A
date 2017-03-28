# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0036_userdefinedclass_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='answer',
            field=models.ForeignKey(related_name='comments_parent_answer', default=0, to='App.Answer'),
        ),
    ]
