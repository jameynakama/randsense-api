# Generated by Django 3.2.6 on 2021-08-13 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randsense', '0012_frequencysettings_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='frequencysettings',
            name='adverbs',
            field=models.BigIntegerField(default=50000),
        ),
    ]