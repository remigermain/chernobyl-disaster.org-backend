# Generated by Django 3.1.1 on 2020-10-01 10:21

from django.db import migrations, models
import django.db.models.deletion
import gallery.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('born', models.DateField(blank=True, null=True)),
                ('death', models.DateField(blank=True, null=True)),
                ('profil', models.ImageField(blank=True, null=True, upload_to=gallery.models.profil_path)),
                ('wikipedia', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PeopleLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Français')], max_length=4)),
                ('biography', models.TextField()),
            ],
            options={
                'ordering': ['language', '-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('have_second', models.BooleanField(default=False)),
                ('have_minute', models.BooleanField(default=False)),
                ('have_hour', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=50)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('picture', models.ImageField(upload_to=gallery.models.picture_path)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PictureLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Français')], max_length=4)),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['language', '-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('have_second', models.BooleanField(default=False)),
                ('have_minute', models.BooleanField(default=False)),
                ('have_hour', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=50)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('video', models.URLField(unique=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='VideoLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Français')], max_length=4)),
                ('title', models.CharField(max_length=50)),
                ('extra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langs', to='gallery.video')),
            ],
            options={
                'ordering': ['language', '-id'],
                'abstract': False,
            },
        ),
    ]
