# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('makesense', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='total_usage',
            field=models.IntegerField(default=0),
        ),
    ]
