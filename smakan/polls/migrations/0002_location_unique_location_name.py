# Generated by Django 4.0.5 on 2022-07-06 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='location',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_location_name'),
        ),
    ]
