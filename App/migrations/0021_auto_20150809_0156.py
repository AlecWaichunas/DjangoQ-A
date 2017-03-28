# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0020_auto_20150809_0051'),
    ]

    operations = [
        migrations.CreateModel(
            name='AVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(null=True)),
                ('answer', models.ForeignKey(related_name='avote_answer', default=0, to='App.Answer')),
                ('user', models.ForeignKey(related_name='avote_user', default=0, to='App.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='QVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(null=True)),
                ('question', models.ForeignKey(related_name='qvote_question', default=0, to='App.Question')),
                ('user', models.ForeignKey(related_name='qvote_user', default=0, to='App.UserProfile')),
            ],
        ),
        migrations.RemoveField(
            model_name='vote',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='user',
        ),
        migrations.AlterField(
            model_name='viewer',
            name='question',
            field=models.ForeignKey(related_name='viewer_question', default=0, to='App.Question'),
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
        migrations.DeleteModel(
            name='Voter',
        ),
    ]
