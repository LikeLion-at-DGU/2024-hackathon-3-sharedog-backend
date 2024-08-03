# Generated by Django 5.0.7 on 2024-08-03 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=255)),
                ('uid', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('provider', 'uid')},
            },
        ),
    ]
