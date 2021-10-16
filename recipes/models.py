import pathlib
import uuid

import pint
from django.db import models
from django.db.models import Q
from django.urls import reverse
from users.models import User

from .utils import number_str_to_float
from .validators import validate_unit_of_measure


class RecipeQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        # lookups = (active=True)
        lookups = (
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(directions__icontains=query)
        )
        return self.filter(lookups)


class RecipeManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Recipe(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    objects = RecipeManager()

    @property
    def title(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipes:detail_view", kwargs={"id": self.id})

    def get_hx_url(self):
        return reverse("recipes:detail_hx", kwargs={"id": self.id})

    def get_update_url(self):
        return reverse("recipes:update_view", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("recipes:delete", kwargs={"id": self.id})

    def get_image_upload_url(self):
        kwarg = {"parent_id": self.id}
        return reverse("recipes:upload_image", kwargs=kwarg)

    def get_ingredients_children(self):
        return self.recipeingredient_set.all()

    class Meta:
        db_table = "recipe_recipe"

    def __str__(self):
        return f"{self.id} | {self.name}"


def recipe_ingredient_image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1())
    return f"recipes/ingredient/{new_fname}{fpath.suffix}"


class RecipeIngredientImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=recipe_ingredient_image_upload_handler)
    extracted = models.JSONField(blank=True, null=True)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    quantity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(
        max_length=50, validators=[validate_unit_of_measure]
    )
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit.lower()]
        print(measurement)
        return measurement  # .to_base_units()

    def as_mks(self):
        measurement = self.convert_to_system(system="mks")
        print(measurement)
        return measurement.to_base_units()

    def as_imperial(self):
        measurement = self.convert_to_system(system="imperial")
        print(measurement)
        return measurement.to_base_units()

    def save(self, *args, **kwargs):
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()

    def get_delete_url(self):
        kwarg = {"parent_id": self.recipe.id, "id": self.id}
        return reverse("recipes:ingredient_delete", kwargs=kwarg)

    def get_hx_edit_url(self):
        kwarg = {"parent_id": self.recipe.id, "id": self.id}
        return reverse("recipes:ingredient_update_hx", kwargs=kwarg)

    class Meta:
        db_table = "recipe_recipe_ingredient"

    def __str__(self):
        return f"{self.id} | {self.name}"
