# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=200)),
                ('question_title', models.CharField(max_length=50)),
                ('views', models.IntegerField(default=0)),
                ('asker', models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='UserDefinedClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('is_private', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(verbose_name=b'date published')),
                ('members', models.ManyToManyField(default=0, related_name='userdefinedclass_members', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(related_name='userdefinedclass_owner', default=0, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('classes', models.ManyToManyField(default=0, related_name='userprofile_classes', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(related_name='userprofile_user', default=0, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
