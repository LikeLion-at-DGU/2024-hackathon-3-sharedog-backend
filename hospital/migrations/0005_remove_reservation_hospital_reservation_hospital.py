# Generated by Django 5.0.7 on 2024-07-27 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_hospital_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='hospital',
        ),
        migrations.AddField(
            model_name='reservation',
            name='hospital',
            field=models.ManyToManyField(to='hospital.hospital'),
        ),
    ]
