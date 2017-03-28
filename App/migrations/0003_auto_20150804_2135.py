# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_auto_20150804_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdefinedclass',
            name='date_created',
            field=models.DateTimeField(),
        ),
    ]
