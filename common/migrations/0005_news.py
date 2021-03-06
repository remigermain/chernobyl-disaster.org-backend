# Generated by Django 3.1.1 on 2020-10-12 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20201009_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('date', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
    ]
