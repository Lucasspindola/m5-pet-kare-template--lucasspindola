# Generated by Django 4.1.6 on 2023-02-09 20:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("traits", "0003_remove_trait_pets"),
        ("pets", "0003_rename_traits_pet_traits_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pet",
            name="traits_name",
        ),
        migrations.AddField(
            model_name="pet",
            name="trait_name",
            field=models.ManyToManyField(related_name="pets", to="traits.trait"),
        ),
    ]
