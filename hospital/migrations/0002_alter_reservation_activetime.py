# Generated by Django 5.0.7 on 2024-08-04 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='activeTime',
            field=models.CharField(choices=[('10:00', '10시'), ('13:00', '13시'), ('15:00', '15시')], max_length=5),
        ),
    ]
