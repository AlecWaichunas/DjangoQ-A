# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0019_auto_20150808_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='reason_text',
        ),
        migrations.AddField(
            model_name='answer',
            name='date_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='date_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vote',
            name='answer',
            field=models.ForeignKey(related_name='vote_answer', default=0, to='App.UserProfile'),
        ),
        migrations.AddField(
            model_name='vote',
            name='date_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='vote',
            name='question',
            field=models.ForeignKey(related_name='vote_question', default=0, to='App.Question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answerer',
            field=models.ForeignKey(related_name='answer_answerer', default=0, to='App.UserProfile'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_title',
            field=models.CharField(max_length=60),
        ),
    ]
