# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0047_assignments_is_anon'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=2)),
                ('classes', models.ManyToManyField(default=0, related_name='school_questions', to='App.Question')),
            ],
        ),
        migrations.AddField(
            model_name='userdefinedclass',
            name='school',
            field=models.ForeignKey(related_name='userdefinedclass_school', default=0, to='App.School'),
        ),
    ]
