# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('makesense', '0005_page_secondary_graphic'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='about',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='acknowledgements',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='introduction',
            field=models.TextField(blank=True),
        ),
    ]
