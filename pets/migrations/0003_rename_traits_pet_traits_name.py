# Generated by Django 4.1.6 on 2023-02-09 20:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0002_pet_traits"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pet",
            old_name="traits",
            new_name="traits_name",
        ),
    ]