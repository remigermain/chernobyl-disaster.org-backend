# Generated by Django 3.1.1 on 2020-10-15 09:17

from django.db import migrations, models
import django.db.models.deletion
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_news_is_active'),
        ('gallery', '0007_remove_picture_photographer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='People',
            new_name='Character',
        ),
        migrations.RenameModel(
            old_name='PeopleLang',
            new_name='CharacterLang',
        ),
    ]
