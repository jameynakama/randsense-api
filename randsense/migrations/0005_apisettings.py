# Generated by Django 3.2.6 on 2021-08-06 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("randsense", "0004_auto_20210806_2033"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApiSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("base_word_frequency", models.BigIntegerField(default=1000000)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]