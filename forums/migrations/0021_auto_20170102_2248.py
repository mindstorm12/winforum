# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-02 22:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0020_auto_20170102_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='forumSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=90)),
                ('idForumCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forums.forumCategory')),
            ],
        ),
        migrations.RemoveField(
            model_name='forumpost',
            name='category',
        ),
        migrations.AddField(
            model_name='forumpost',
            name='forumSubCategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
                                    to='forums.forumSubCategory'),
            preserve_default=False,
        ),
    ]
