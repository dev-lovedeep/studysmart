# Generated by Django 3.0.2 on 2020-01-27 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='imagesrc',
            field=models.CharField(max_length=120),
        ),
    ]