# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0029_auto_20150812_0515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=6000)),
                ('title', models.CharField(max_length=60)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('views', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('is_anon', models.BooleanField(default=False)),
                ('parent_class', models.ForeignKey(related_name='discussion_parent_class', default=0, to='App.UserDefinedClass')),
                ('poster', models.ForeignKey(default=0, to='App.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Replies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=5000)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('points', models.IntegerField(default=0)),
                ('is_anon', models.BooleanField(default=False)),
                ('discussion', models.ForeignKey(related_name='replies_discussion', default=0, to='App.Discussion')),
                ('replier', models.ForeignKey(related_name='replies_answerer', default=0, to='App.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='avote',
            name='is_negative',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answer_parent_question', default=0, to='App.Question'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='replies',
            field=models.ManyToManyField(default=0, related_name='discussion_replies', to='App.Replies'),
        ),
    ]
