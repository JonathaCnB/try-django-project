from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ["id", "title", "content"]
    search_fields = ["title", "content"]
