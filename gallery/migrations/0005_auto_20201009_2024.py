# Generated by Django 3.1.1 on 2020-10-09 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_auto_20201009_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]