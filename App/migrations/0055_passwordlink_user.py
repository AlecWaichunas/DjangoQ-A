# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0054_passwordlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordlink',
            name='user',
            field=models.ForeignKey(related_name='passwordlink_user', default=0, to='App.UserProfile'),
        ),
    ]
