# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0017_voter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ForeignKey(to='App.Question')),
                ('user', models.ForeignKey(to='App.UserProfile')),
            ],
        ),
        migrations.RemoveField(
            model_name='userdefinedclass',
            name='views',
        ),
    ]
