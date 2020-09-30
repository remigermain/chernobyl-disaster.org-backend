# Generated by Django 3.1.1 on 2020-09-30 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Translate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(blank=True, unique=True)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TagLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Français')], max_length=4)),
                ('name', models.CharField(max_length=50)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langs', to='common.tag')),
            ],
            options={
                'ordering': ['language', '-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TranslateLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Français')], max_length=4)),
                ('value', models.TextField()),
                ('parent_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langs', to='common.translate')),
            ],
            options={
                'ordering': ['-id'],
                'unique_together': {('parent_key', 'language')},
            },
        ),
    ]
