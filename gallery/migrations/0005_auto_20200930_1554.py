# Generated by Django 3.1.1 on 2020-09-30 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_auto_20200930_1510'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-id']},
        ),
    ]
