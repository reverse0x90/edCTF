# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'category',
            },
        ),
        migrations.CreateModel(
            name='challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('points', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=500)),
                ('num_solved', models.IntegerField(default=0)),
                ('category', models.ForeignKey(to='api.category')),
            ],
            options={
                'verbose_name_plural': 'challenges',
            },
        ),
        migrations.CreateModel(
            name='challengeboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'challengeboard',
            },
        ),
        migrations.CreateModel(
            name='ctf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('live', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'ctfs',
            },
        ),
        migrations.CreateModel(
            name='scoreboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numtopteams', models.IntegerField(default=10)),
                ('ctf', models.OneToOneField(to='api.ctf')),
            ],
            options={
                'verbose_name_plural': 'scoreboards',
            },
        ),
        migrations.CreateModel(
            name='team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teamname', models.CharField(unique=True, max_length=20)),
                ('points', models.IntegerField(default=0)),
                ('correct_flags', models.IntegerField(default=0)),
                ('wrong_flags', models.IntegerField(default=0)),
                ('scoreboard', models.ForeignKey(to='api.scoreboard')),
            ],
            options={
                'verbose_name_plural': 'teams',
            },
        ),
        migrations.AddField(
            model_name='challengeboard',
            name='ctf',
            field=models.OneToOneField(to='api.ctf'),
        ),
        migrations.AddField(
            model_name='category',
            name='challengeboard',
            field=models.ForeignKey(to='api.challengeboard'),
        ),
    ]
