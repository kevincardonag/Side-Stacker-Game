# Generated by Django 3.2.6 on 2021-08-28 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("boards", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="number_of_movements",
            field=models.IntegerField(default=0, verbose_name="Number of movements"),
        ),
    ]