# Generated by Django 5.0.7 on 2024-07-26 23:19

import hospital.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_alter_dog_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=hospital.models.image_upload_path),
        ),
    ]
