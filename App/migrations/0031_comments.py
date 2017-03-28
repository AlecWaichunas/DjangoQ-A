# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0030_auto_20150812_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=3000)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('points', models.IntegerField(default=0)),
                ('is_anon', models.BooleanField(default=False)),
                ('answer', models.ForeignKey(related_name='comments_parent_answer', default=0, to='App.Question')),
                ('commenter', models.ForeignKey(related_name='comments_comenter', default=0, to='App.UserProfile')),
            ],
        ),
    ]
