# Generated by Django 2.1.2 on 2019-03-06 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0027_profile_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='favorites',
            field=models.ManyToManyField(blank=True, to='reservations.Resource'),
        ),
    ]
