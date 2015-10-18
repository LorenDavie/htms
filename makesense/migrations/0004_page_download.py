# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('makesense', '0003_auto_20151018_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='download',
            field=models.URLField(null=True),
        ),
    ]
