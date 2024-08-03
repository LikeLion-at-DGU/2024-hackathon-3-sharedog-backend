# Generated by Django 5.0.7 on 2024-08-04 01:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agetest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('age_group', models.CharField(choices=[('UNDER_18M', '18개월 미만'), ('18M_TO_8Y', '18개월~8살'), ('OVER_9Y', '9살 이상')], max_length=10)),
                ('writer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Diseasetest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('has_disease', models.CharField(choices=[('YES', '네'), ('NO', '아니요')], max_length=3)),
                ('writer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sizetest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('size', models.CharField(choices=[('SM', '소형견'), ('LG', '대형견')], max_length=2)),
                ('writer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccinetest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_vaccinated', models.CharField(choices=[('YES', '네'), ('NO', '아니요')], max_length=3)),
                ('writer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Weighttest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('weight_group', models.CharField(choices=[('UNDER_20KG', '20kg 이하'), ('OVER_20KG', '20kg 이상')], max_length=10)),
                ('writer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Totaltest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('age_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.agetest')),
                ('has_disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.diseasetest')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sizetest')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('is_vaccinated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.vaccinetest')),
                ('weight_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.weighttest')),
            ],
        ),
    ]
