from django.urls import path
from meals import views as meal_views

from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.recipe_list_view, name="recipe_list"),
    path("create/", views.recipe_create_view, name="create_view"),
    path(
        "meal-toggle/<int:recipe_id>/",
        meal_views.meal_queue_toggle_view,
        name="meal_toggle",
    ),
    path("update/<int:id>/", views.recipe_update_view, name="update_view"),
    path("detail/<int:id>/", views.recipe_detail_view, name="detail_view"),
    path("delete/<int:id>/", views.recipe_delete_view, name="delete"),
    path(
        "upload-image/<int:parent_id>/",
        views.recipe_ingredient_image_upload_view,
        name="upload_image",
    ),
    path(
        "<int:parent_id>/ingredient/<int:id>/",
        views.recipe_ingredient_delete_view,
        name="ingredient_delete",
    ),
    path(
        "hx/<int:parent_id>/ingredient/<int:id>/",
        views.recipe_ingredient_update_hx_view,
        name="ingredient_update_hx",
    ),
    path(
        "hx/<int:parent_id>/ingredient/",
        views.recipe_ingredient_update_hx_view,
        name="ingredient_create_hx",
    ),
    path("hx/<int:id>/", views.recipe_detail_hx_view, name="detail_hx"),
]
