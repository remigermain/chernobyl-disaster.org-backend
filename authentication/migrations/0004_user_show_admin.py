# Generated by Django 3.1.1 on 2020-10-11 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20201009_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='show_admin',
            field=models.BooleanField(default=False),
        ),
    ]
