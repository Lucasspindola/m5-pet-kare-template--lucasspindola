# Generated by Django 4.1.6 on 2023-02-09 18:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("traits", "0003_remove_trait_pets"),
        ("pets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pet",
            name="traits",
            field=models.ManyToManyField(related_name="pets", to="traits.trait"),
        ),
    ]
