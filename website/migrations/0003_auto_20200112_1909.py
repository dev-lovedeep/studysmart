# Generated by Django 3.0.2 on 2020-01-12 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20200111_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='contact',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]