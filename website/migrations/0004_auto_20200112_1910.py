# Generated by Django 3.0.2 on 2020-01-12 13:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20200112_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='contact',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]
