# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0024_auto_20150810_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdefinedclass',
            name='members',
            field=models.ManyToManyField(default=0, related_name='userdefinedclass_members', to='App.UserProfile'),
        ),
    ]
