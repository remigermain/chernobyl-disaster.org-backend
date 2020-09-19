# Generated by Django 3.1.1 on 2020-09-19 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_translate_translatelang'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translatelang',
            name='translate',
        ),
        migrations.AddField(
            model_name='translatelang',
            name='key',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='langs', to='common.translate'),
            preserve_default=False,
        ),
    ]
