from django.contrib import admin

from .models import Meal


@admin.register(Meal)
class ArticleAdmin(admin.ModelAdmin):
    model = Meal
    list_display = ["id", "user", "recipe", "status", "timestamp", "update"]
    search_fields = ["user", "recipe"]
