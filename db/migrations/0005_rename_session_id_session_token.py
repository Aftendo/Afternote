# Generated by Django 4.1.7 on 2024-01-14 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_user_ban'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='session_id',
            new_name='token',
        ),
    ]
