from django.contrib import admin

from .models import Recipe, RecipeIngredient, RecipeIngredientImage


class RecipeIngredientInLine(admin.StackedInline):
    model = RecipeIngredient
    readonly_fields = ["quantity_as_float", "as_mks", "as_imperial"]
    # fields = ["name", "quantity", "unit", "quantity_as_float", "directions"]
    raw_id_fields = ["recipe"]
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    inlines = [RecipeIngredientInLine]
    list_display = ["id", "user", "name", "timestamp", "update", "active"]
    search_fields = ["name", "description"]
    raw_id_fields = ["user"]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    model = RecipeIngredient
    list_display = ["id", "recipe", "name", "timestamp", "update"]
    search_fields = ["name", "description"]


@admin.register(RecipeIngredientImage)
class RecipeIngredientImageAdmin(admin.ModelAdmin):
    model = RecipeIngredientImage
    list_display = ["id", "recipe", "image"]
    search_fields = ["recipe"]
