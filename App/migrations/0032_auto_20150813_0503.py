# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0031_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdefinedclass',
            name='owner',
            field=models.ForeignKey(related_name='userdefinedclass_owner', default=0, to='App.UserProfile'),
        ),
    ]
