# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0043_auto_20150818_0236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_negative', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='vote_user', default=0, to='App.UserProfile')),
            ],
        ),
        migrations.RemoveField(
            model_name='avote',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='avote',
            name='user',
        ),
        migrations.DeleteModel(
            name='AVote',
        ),
        migrations.AddField(
            model_name='answer',
            name='votes',
            field=models.ManyToManyField(default=0, related_name='answer_votes', to='App.Vote'),
        ),
    ]
