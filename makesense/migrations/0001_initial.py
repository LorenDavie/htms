# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djax.content


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('dedication', models.TextField(blank=True)),
            ],
            bases=(models.Model, djax.content.ACEContent),
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('book', models.ForeignKey(related_name='chapters', to='makesense.Book')),
            ],
            bases=(models.Model, djax.content.ACEContent),
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField(blank=True)),
            ],
            bases=(models.Model, djax.content.ACEContent),
        ),
        migrations.CreateModel(
            name='Excercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField(blank=True)),
            ],
            bases=(models.Model, djax.content.ACEContent),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('body', models.TextField()),
                ('graphic', models.URLField(max_length=400, null=True, blank=True)),
                ('chapter', models.ForeignKey(related_name='pages', to='makesense.Chapter')),
            ],
            bases=(models.Model, djax.content.ACEContent),
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=100)),
                ('word_type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('usage', models.ManyToManyField(related_name='terms', to='makesense.Page')),
            ],
            options={
                'ordering': ['term'],
            },
            bases=(models.Model, djax.content.ACEContent),
        ),
        migrations.CreateModel(
            name='TermAlternative',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alternative_term', models.CharField(max_length=100)),
                ('term', models.ForeignKey(related_name='alternatives', to='makesense.Term')),
            ],
        ),
        migrations.CreateModel(
            name='WorkSheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('downloadable', models.URLField(max_length=400, blank=True)),
                ('image', models.URLField(max_length=400, blank=True)),
            ],
            bases=(models.Model, djax.content.ACEContent),
        ),
        migrations.AddField(
            model_name='chapter',
            name='example',
            field=models.ForeignKey(to='makesense.Example', unique=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='excercise',
            field=models.ForeignKey(to='makesense.Excercise', unique=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='worksheet',
            field=models.ForeignKey(to='makesense.WorkSheet', unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='termalternative',
            unique_together=set([('term', 'alternative_term')]),
        ),
        migrations.AlterUniqueTogether(
            name='term',
            unique_together=set([('term', 'word_type')]),
        ),
    ]
