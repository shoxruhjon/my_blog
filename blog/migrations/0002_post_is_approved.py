# Generated by Django 5.1.3 on 2024-11-19 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
