# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0058_userprofile_is_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassConfirmLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(default=0, max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('single_class', models.ForeignKey(related_name='classconfirmlink_class', default=0, to='App.UserDefinedClass')),
                ('user', models.ForeignKey(related_name='classconfirmlink_user', default=0, to='App.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='confirmlink',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
