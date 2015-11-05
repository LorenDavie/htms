# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('makesense', '0004_page_download'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='secondary_graphic',
            field=models.URLField(max_length=400, null=True, blank=True),
        ),
    ]
