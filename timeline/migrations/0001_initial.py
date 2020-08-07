# Generated by Django 3.0.8 on 2020-08-07 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import timeline.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('link', models.URLField(unique=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('doc', models.FileField(upload_to=timeline.models.document_path)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField(unique=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_creator', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='events', to='common.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('picture', models.ImageField(upload_to=timeline.models.picture_path)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='picture_creator', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='picture_event', to='timeline.Event')),
                ('photographer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pictures', to='common.People')),
                ('tags', models.ManyToManyField(blank=True, related_name='picture_extra', to='common.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('video', models.URLField(unique=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='video_creator', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='video_event', to='timeline.Event')),
                ('tags', models.ManyToManyField(blank=True, related_name='video_extra', to='common.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Français')], default='en', max_length=4)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='videolang_creator', to=settings.AUTH_USER_MODEL)),
                ('extra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langs', to='timeline.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PictureLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Français')], default='en', max_length=4)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='picturelang_creator', to=settings.AUTH_USER_MODEL)),
                ('extra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langs', to='timeline.Picture')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Français')], default='en', max_length=4)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eventlang_creator', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langs', to='timeline.Event')),
            ],
            options={
                'ordering': ['language'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Français')], default='en', max_length=4)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documentlang_creator', to=settings.AUTH_USER_MODEL)),
                ('extra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langs', to='timeline.Document')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='document',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document_event', to='timeline.Event'),
        ),
        migrations.AddField(
            model_name='document',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='document_extra', to='common.Tag'),
        ),
        migrations.CreateModel(
            name='ArticleLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Français')], default='en', max_length=4)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articlelang_creator', to=settings.AUTH_USER_MODEL)),
                ('extra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='langs', to='timeline.Article')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='article',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_event', to='timeline.Event'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='article_extra', to='common.Tag'),
        ),
    ]
