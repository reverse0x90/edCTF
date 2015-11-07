# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teamname', models.CharField(unique=True, max_length=20)),
                ('points', models.IntegerField(default=0)),
                ('correct_flags', models.IntegerField(default=0)),
                ('wrong_flags', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'teams',
            },
        ),
    ]
