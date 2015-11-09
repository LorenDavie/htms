# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('makesense', '0006_auto_20151109_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='resources',
            field=models.TextField(blank=True),
        ),
    ]
