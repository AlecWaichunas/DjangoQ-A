# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0026_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='user',
            field=models.ForeignKey(related_name='notifications_user', default=0, to='App.UserProfile'),
        ),
    ]
