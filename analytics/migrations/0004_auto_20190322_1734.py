# Generated by Django 2.1.2 on 2019-03-22 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0029_auto_20190322_1323'),
        ('analytics', '0003_auto_20190322_1730'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TotalsSinceCreation',
            new_name='LifetimeAionStats',
        ),
        migrations.RenameModel(
            old_name='TotalsPerSchool',
            new_name='LifetimeSchoolStats',
        ),
    ]
