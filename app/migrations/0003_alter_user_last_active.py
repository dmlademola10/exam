# Generated by Django 4.1 on 2023-01-22 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="last_active",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
