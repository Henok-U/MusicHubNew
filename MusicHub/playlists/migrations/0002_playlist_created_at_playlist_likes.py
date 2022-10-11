# Generated by Django 4.1 on 2022-10-11 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playlist',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]