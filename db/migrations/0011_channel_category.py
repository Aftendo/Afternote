# Generated by Django 4.1.7 on 2024-01-14 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0010_category_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='db.category'),
            preserve_default=False,
        ),
    ]
