# Generated by Django 2.1.2 on 2019-02-19 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0025_auto_20190219_1536'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Email_Filters',
            new_name='EmailFilter',
        ),
    ]
