# Generated by Django 2.1.2 on 2019-01-30 00:12

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('reservations', '0014_auto_20190129_1334'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Block',
            new_name='TimeBlock',
        ),
        migrations.AlterModelOptions(
            name='timeblock',
            options={'ordering': ['sequence', 'name']},
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='block',
            new_name='time_block',
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('resource', 'time_block', 'date')},
        ),
    ]
