# Generated by Django 3.2.6 on 2021-08-21 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='room_name',
            field=models.CharField(default=1, max_length=255, verbose_name='Room name'),
            preserve_default=False,
        ),
    ]
