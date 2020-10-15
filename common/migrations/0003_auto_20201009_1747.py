# Generated by Django 3.1.1 on 2020-10-09 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20201007_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taglang',
            name='language',
            field=models.CharField(choices=[('de', 'Deutsch'), ('en', 'English'), ('es', 'Español'), ('fr', 'Français'), ('it', 'Italiano'), ('ja', '日本語 (にほんご)'), ('ru', 'русский'), ('uk', 'Українська'), ('zh', '漢語')], max_length=4),
        ),
        migrations.AlterField(
            model_name='translatelang',
            name='language',
            field=models.CharField(choices=[('de', 'Deutsch'), ('en', 'English'), ('es', 'Español'), ('fr', 'Français'), ('it', 'Italiano'), ('ja', '日本語 (にほんご)'), ('ru', 'русский'), ('uk', 'Українська'), ('zh', '漢語')], max_length=4),
        ),
    ]