# Generated by Django 4.1.7 on 2024-01-14 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_flipnote_saved_flipnote_views_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flipnote',
            name='saved',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flipnote',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
