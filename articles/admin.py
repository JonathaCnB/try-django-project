from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ["id", "title", "slug", "content", "timestamp", "update"]
    search_fields = ["title", "content"]
