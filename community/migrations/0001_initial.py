<<<<<<< HEAD
# Generated by Django 5.0.7 on 2024-08-03 12:47
=======
# Generated by Django 5.0.7 on 2024-08-03 12:24
>>>>>>> 9e9e013c75ddb9fb5c36e292d4163d504e0cf5ae

import community.models
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
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=300)),
                ('region', models.CharField(choices=[(None, '지역'), ('서울', '서울'), ('경기', '경기'), ('인천', '인천'), ('강원', '강원'), ('경상', '경상'), ('충청', '충청'), ('전라', '전라'), ('제주', '제주')], default='지역', max_length=50)),
                ('blood', models.CharField(choices=[(None, '혈액형'), ('DEA 1-', 'DEA 1-'), ('DEA 1.1', 'DEA 1.1'), ('DEA 1.2', 'DEA 1.2'), ('DEA 3', 'DEA 3'), ('DEA 4', 'DEA 4'), ('DEA 5', 'DEA 5'), ('DEA 6', 'DEA 6'), ('DEA 7', 'DEA 7')], default='혈액형', max_length=30)),
                ('image_1', models.ImageField(blank=True, null=True, upload_to=community.models.image_upload_path)),
                ('image_2', models.ImageField(blank=True, null=True, upload_to=community.models.image_upload_path)),
                ('image_3', models.ImageField(blank=True, null=True, upload_to=community.models.image_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('like_num', models.PositiveIntegerField(default=0)),
                ('like', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='community.post')),
            ],
        ),
        migrations.CreateModel(
            name='Recomment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recomments', to='community.comment')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
