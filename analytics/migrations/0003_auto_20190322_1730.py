# Generated by Django 2.1.2 on 2019-03-22 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0029_auto_20190322_1323'),
        ('analytics', '0002_auto_20190322_1726'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='totalsperschool',
            options={'ordering': ['organization', 'school']},
        ),
        migrations.AddField(
            model_name='totalsperschool',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservations.Organization'),
        ),
    ]
