# Generated by Django 5.0.7 on 2024-08-05 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agetest',
            old_name='writer',
            new_name='nickname',
        ),
        migrations.RenameField(
            model_name='diseasetest',
            old_name='writer',
            new_name='nickname',
        ),
        migrations.RenameField(
            model_name='sizetest',
            old_name='writer',
            new_name='nickname',
        ),
        migrations.RenameField(
            model_name='totaltest',
            old_name='writer',
            new_name='nickname',
        ),
        migrations.RenameField(
            model_name='vaccinetest',
            old_name='writer',
            new_name='nickname',
        ),
        migrations.RenameField(
            model_name='weighttest',
            old_name='writer',
            new_name='nickname',
        ),
    ]
