# Generated by Django 4.1.7 on 2024-01-14 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0009_flipnote_made_by_alter_user_fsid_alter_user_mac'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('internal_id', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('internal_id', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
    ]