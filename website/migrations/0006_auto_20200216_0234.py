# Generated by Django 3.0.2 on 2020-02-15 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_download_haspaper'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='download',
            name='haspaper',
        ),
        migrations.AddField(
            model_name='subject_names',
            name='haspaper',
            field=models.BooleanField(default=True),
        ),
    ]