# Generated by Django 5.1.3 on 2024-11-23 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_group_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
