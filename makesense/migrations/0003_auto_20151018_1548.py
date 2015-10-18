# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('makesense', '0002_term_total_usage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='example',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='excercise',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='worksheet',
        ),
        migrations.AddField(
            model_name='page',
            name='is_supporting_material',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='page',
            name='supporting_material_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Example',
        ),
        migrations.DeleteModel(
            name='Excercise',
        ),
        migrations.DeleteModel(
            name='WorkSheet',
        ),
    ]
