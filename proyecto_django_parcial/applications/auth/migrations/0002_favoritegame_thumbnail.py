# Generated by Django 5.2.1 on 2025-05-20 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritegame',
            name='thumbnail',
            field=models.URLField(blank=True),
        ),
    ]
