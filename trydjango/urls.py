from django.contrib import admin
from django.urls import include, path
from users.views import login_view, logout_view, register_view

urlpatterns = [
    path("", include("articles.urls")),
    path("search/", include("search.urls")),
    path("recipes/", include("recipes.urls")),
    path("login/", login_view),
    path("logout/", logout_view),
    path("register/", register_view),
    path("admin/", admin.site.urls),
]
