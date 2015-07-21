# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acceptance_criteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descr', models.CharField(max_length=500)),
                ('title', models.CharField(max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Backlog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_id_fk', models.IntegerField(null=True)),
                ('story_title', models.CharField(max_length=50)),
                ('story_descr', models.CharField(max_length=2000, null=True)),
                ('priority', models.CharField(default=b'9', max_length=1, null=True)),
                ('module', models.CharField(max_length=50, null=True)),
                ('skills', models.CharField(max_length=50, null=True)),
                ('notes', models.CharField(max_length=2000, null=True)),
                ('github_number', models.CharField(max_length=5, null=True)),
                ('github_repo', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('schedule_id_fk', models.IntegerField(null=True)),
                ('start_dttm', models.DateField(null=True)),
                ('end_dttm', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=12)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('focus', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=250, null=True)),
                ('visibility', models.CharField(default=b'Private', max_length=10)),
                ('task_manager_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='backlog',
            name='sprint',
            field=models.ForeignKey(to='core.Event', db_column=b'sprint_id_fk'),
        ),
        migrations.AddField(
            model_name='backlog',
            name='status',
            field=models.ForeignKey(to='core.Status', db_column=b'status_id_fk'),
        ),
        migrations.AddField(
            model_name='backlog',
            name='team',
            field=models.ForeignKey(to='core.Team', db_column=b'team_id_fk'),
        ),
        migrations.AddField(
            model_name='acceptance_criteria',
            name='backlog',
            field=models.ForeignKey(to='core.Backlog', db_column=b'backlog_id_fk'),
        ),
    ]
