from django.core.exceptions import ValidationError
from django.test import TestCase
from users.models import User

from .models import Recipe, RecipeIngredient


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user("cfe", password="abc123")
        self.recipe_a = Recipe.objects.create(
            name="Frango frito",
            user=self.user_a,
        )
        self.recipe_a = Recipe.objects.create(
            name="Frango frito apimentado",
            user=self.user_a,
        )
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name="Frango",
            quantity="1/2",
            unit="kg",
        )
        self.recipe_ingredient_b = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name="Frango",
            quantity="negado",
            unit="kg",
        )

    # def test_user_recipe_count(self):
    #     user = self.user_a
    #     qs = user.recipe_set.all()
    #     self.assertEqual(qs.count(), 0)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user=user)
        self.assertEqual(qs.count(), 2)

    def test_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all()
        self.assertEqual(qs.count(), 2)

    def test_recipe_ingredient_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation(self):
        user = self.user_a
        qs = RecipeIngredient.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation_reverse(self):
        user = self.user_a
        recipeingredient_ids = list(
            user.recipe_set.all().values_list(
                "recipeingredient__id",
                flat=True,
            )
        )
        qs = RecipeIngredient.objects.filter(id__in=recipeingredient_ids)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipe_set.all().values_list("id", flat=True)
        qs = RecipeIngredient.objects.filter(recipe__id__in=ids)
        self.assertEqual(qs.count(), 2)

    def test_unit_measure_validation(self):
        invalid_unit = "kg"
        ingredient = RecipeIngredient(
            name="New",
            quantity=10,
            recipe=self.recipe_a,
            unit=invalid_unit,
        )
        ingredient.full_clean()

    def test_unit_measure_validation_error(self):
        invalid_units = ["nada", "coisa"]
        with self.assertRaises(ValidationError):
            for unit in invalid_units:
                ingredient = RecipeIngredient(
                    name="New",
                    quantity=10,
                    recipe=self.recipe_a,
                    unit=unit,
                )
                ingredient.full_clean()

    def test_quantity_as_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)
