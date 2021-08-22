# Generated by Django 3.2.6 on 2021-08-21 15:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("boards", "0002_game_room_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="board",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django.contrib.postgres.fields.ArrayField(
                    base_field=models.CharField(blank=True, max_length=10, null=True),
                    size=6,
                ),
                blank=True,
                size=6,
            ),
        ),
    ]
