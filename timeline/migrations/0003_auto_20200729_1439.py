# Generated by Django 3.0.8 on 2020-07-29 14:39

from django.db import migrations, models
import timeline.models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0002_auto_20200726_1755'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='event',
            name='event_date_unique',
        ),
        migrations.RenameField(
            model_name='picture',
            old_name='image',
            new_name='picture',
        ),
        migrations.RemoveField(
            model_name='document',
            name='image',
        ),
        migrations.AlterField(
            model_name='document',
            name='doc',
            field=models.FileField(upload_to=timeline.models.fnc_extra_path),
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together={('link', 'event')},
        ),
        migrations.AlterUniqueTogether(
            name='articlelang',
            unique_together={('extra', 'language')},
        ),
        migrations.AlterUniqueTogether(
            name='documentlang',
            unique_together={('extra', 'language')},
        ),
        migrations.AlterUniqueTogether(
            name='eventlang',
            unique_together={('language', 'event')},
        ),
        migrations.AlterUniqueTogether(
            name='picturelang',
            unique_together={('extra', 'language')},
        ),
        migrations.AlterUniqueTogether(
            name='video',
            unique_together={('video', 'event')},
        ),
        migrations.AlterUniqueTogether(
            name='videolang',
            unique_together={('extra', 'language')},
        ),
        migrations.AddConstraint(
            model_name='article',
            constraint=models.UniqueConstraint(fields=('link', 'event'), name='article_extra_article'),
        ),
        migrations.AddConstraint(
            model_name='video',
            constraint=models.UniqueConstraint(fields=('video', 'event'), name='video_extra_video'),
        ),
    ]