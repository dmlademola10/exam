# Generated by Django 4.1 on 2023-02-25 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_alter_announcement_added_on"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="added_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]