# Generated by Django 5.0.7 on 2024-08-03 23:14

import django.db.models.deletion
import hospital.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('region', models.CharField(choices=[(None, '지역'), ('서울', '서울'), ('경기', '경기'), ('인천', '인천'), ('강원', '강원'), ('경상', '경상'), ('충청', '충청'), ('전라', '전라'), ('제주', '제주')], default='지역', max_length=50)),
                ('tel_num', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=hospital.models.image_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.dogprofile')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='hospital.hospital')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
