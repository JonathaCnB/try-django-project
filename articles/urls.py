from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path("", views.homepage, name="home"),
    path("articles/", views.article_search_view, name="search_view"),
    path("articles/create/", views.article_create_view, name="create_view"),
    path("articles/<slug:slug>/", views.article_detail_view, name="detail_view"),
]
