# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0060_userdefinedclass_member_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignments',
            name='parent_class',
            field=models.ForeignKey(related_name='assignments_parent_class', default=0, to='App.UserDefinedClass'),
        ),
    ]
