# Generated by Django 4.1 on 2023-01-22 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(default="u", max_length=100),
        ),
    ]
