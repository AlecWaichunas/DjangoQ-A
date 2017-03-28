# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0056_auto_20150826_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(default=0, max_length=128)),
                ('user', models.ForeignKey(related_name='confirmlink_user', default=0, to='App.UserProfile')),
            ],
        ),
    ]
