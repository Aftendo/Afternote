# Generated by Django 4.1.7 on 2024-01-15 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0012_flipnote_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blue_star',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='green_star',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='purple_star',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='red_star',
            field=models.IntegerField(default=0),
        ),
    ]