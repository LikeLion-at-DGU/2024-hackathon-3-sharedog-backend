# Generated by Django 5.0.7 on 2024-07-31 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_dogprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dogprofile',
            name='dog_weight',
            field=models.CharField(max_length=50),
        ),
    ]
