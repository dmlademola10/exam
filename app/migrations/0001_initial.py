# Generated by Django 4.1 on 2023-01-18 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("suspended", models.BooleanField(default=False)),
                ("username", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("last_active", models.DateTimeField()),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]