# Generated by Django 4.2.3 on 2023-11-08 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picks', '0002_remove_game_datetime_game_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pick',
            name='winby',
            field=models.PositiveIntegerField(null=True),
        ),
    ]