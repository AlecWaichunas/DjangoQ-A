# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0021_auto_20150809_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='asker',
            field=models.ForeignKey(default=0, to='App.UserProfile'),
        ),
    ]
