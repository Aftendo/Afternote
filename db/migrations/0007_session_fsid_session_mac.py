# Generated by Django 4.1.7 on 2024-01-14 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_session_temp_alter_session_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='fsid',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='mac',
            field=models.CharField(default='', max_length=12),
            preserve_default=False,
        ),
    ]