# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-16 23:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0026_auto_20170115_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='idForumSubcategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='forums.forumSubCategory'),
        ),
        migrations.AddField(
            model_name='thread',
            name='ifForumCategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='forums.forumCategory'),
        ),
    ]