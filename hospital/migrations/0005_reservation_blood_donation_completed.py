# Generated by Django 5.0.7 on 2024-08-06 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_alter_reservation_activetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='blood_donation_completed',
            field=models.BooleanField(default=False),
        ),
    ]
