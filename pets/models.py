from django.db import models

# Create your models here.


class SexAnimal(models.TextChoices):
    DEFAULT = "Not Informed"
    MALE = "Male"
    FEMALE = "Female"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, default=SexAnimal.DEFAULT, choices=SexAnimal.choices
    )
    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets"
    )
    traits = models.ManyToManyField("traits.Trait", related_name="pets", blank=True)
