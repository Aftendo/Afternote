# Generated by Django 4.1.7 on 2024-01-15 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0013_user_blue_star_user_green_star_user_purple_star_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flipnote',
            name='blue_star',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='flipnote',
            name='green_star',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='flipnote',
            name='purple_star',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='flipnote',
            name='red_star',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='flipnote',
            name='star',
            field=models.IntegerField(default=0),
        ),
    ]