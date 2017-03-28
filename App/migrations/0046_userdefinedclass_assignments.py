# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0045_assignments'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdefinedclass',
            name='assignments',
            field=models.ManyToManyField(default=0, related_name='userdefinedclass_Assignments', to='App.Assignments'),
        ),
    ]
