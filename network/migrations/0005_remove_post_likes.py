# Generated by Django 4.2.9 on 2024-01-15 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
