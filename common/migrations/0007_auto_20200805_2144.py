# Generated by Django 3.0.8 on 2020-08-05 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20200804_0917'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='peoplelang',
            options={'ordering': ['language']},
        ),
        migrations.AlterModelOptions(
            name='taglang',
            options={'ordering': ['language']},
        ),
    ]
