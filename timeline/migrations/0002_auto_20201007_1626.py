# Generated by Django 3.1.1 on 2020-10-07 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlang',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('fr', 'Français'), ('de', 'Deutsch'), ('it', 'Italiano'), ('es', 'Español'), ('uk', 'Українська'), ('ru', 'русский'), ('zh', '漢語'), ('ja', '日本語 (にほんご)')], max_length=4),
        ),
    ]