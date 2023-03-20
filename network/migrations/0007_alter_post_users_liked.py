# Generated by Django 4.1.4 on 2023-03-03 12:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_post_users_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='users_liked',
            field=models.ManyToManyField(blank=True, related_name='posts_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
