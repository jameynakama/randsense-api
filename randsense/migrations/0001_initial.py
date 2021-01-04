# Generated by Django 3.1.4 on 2021-01-03 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('base', models.TextField()),
                ('is_correct', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('attributes', models.JSONField(default=dict)),
            ],
            options={
                'ordering': ('base',),
            },
        ),
    ]
