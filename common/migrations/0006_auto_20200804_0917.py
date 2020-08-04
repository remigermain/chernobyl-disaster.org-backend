# Generated by Django 3.0.8 on 2020-08-04 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20200731_1604'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='peoplelang',
            name='peoplelang_unique',
        ),
        migrations.RemoveConstraint(
            model_name='taglang',
            name='taglang_unique',
        ),
        migrations.AlterUniqueTogether(
            name='peoplelang',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='taglang',
            unique_together=set(),
        ),
    ]
