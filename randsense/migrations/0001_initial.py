# Generated by Django 3.1.5 on 2021-01-10 08:48

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Adverb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Auxiliary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Conjunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Determiner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenericWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Modal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Noun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Preposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pronoun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('base', models.JSONField(blank=True, default=list)),
                ('diagram', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None)),
                ('inflected', models.TextField(blank=True, null=True)),
                ('is_correct', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='SpecialWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Verb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(db_index=True, max_length=255)),
                ('inflections', models.JSONField(blank=True, default=dict)),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-base'],
                'abstract': False,
            },
        ),
    ]
