# Generated by Django 4.2.3 on 2023-11-06 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='datetime',
        ),
        migrations.AddField(
            model_name='game',
            name='date',
            field=models.DateField(default='2023-12-26'),
            preserve_default=False,
        ),
    ]