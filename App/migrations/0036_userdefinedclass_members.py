# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0035_remove_userdefinedclass_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdefinedclass',
            name='members',
            field=models.ManyToManyField(default=0, related_name='userdefinedclass_members', to='App.UserProfile'),
        ),
    ]
