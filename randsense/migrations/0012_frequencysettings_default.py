# Generated by Django 3.2.6 on 2021-08-12 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randsense', '0011_auto_20210812_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='frequencysettings',
            name='default',
            field=models.BigIntegerField(default=1000000),
        ),
    ]
