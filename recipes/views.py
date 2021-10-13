from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientImageForm
from .models import Recipe, RecipeIngredient


@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {"object_list": qs}
    return render(request, "recipes/list.html", context)


@login_required
def recipe_detail_view(request, id=None):
    hx_url = reverse("recipes:detail_hx", kwargs={"id": id})
    context = {"hx_url": hx_url}
    return render(request, "recipes/detail.html", context)


@login_required
def recipe_delete_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except Exception as e:
        print(e)
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse("Não Encontrado")
        raise Http404
    if request.method == "POST":
        obj.active = False
        obj.save()
        success_url = reverse("recipes:recipe_list")
        if request.htmx:
            headers = {"HX-Redirect": success_url}
            return HttpResponse("Deletado", headers=headers)
        return redirect(success_url)
    context = {"object": obj}
    return render(request, "recipes/delete.html", context)


@login_required
def recipe_ingredient_delete_view(request, parent_id=None, id=None):
    try:
        obj = RecipeIngredient.objects.get(
            recipe__id=parent_id, id=id, recipe__user=request.user
        )
    except Exception as e:
        print(e)
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse("Não Encontrado")
        raise Http404
    if request.method == "POST":
        name = obj.name
        obj.active = False
        obj.save()
        success_url = reverse("recipes:detail_view", kwargs={"id": parent_id})
        if request.htmx:
            # headers = {"HX-Redirect": success_url}
            # return HttpResponse("<span style='color: #ccc';>Deletado<span>")
            return render(
                request,
                "recipes/partials/ingredient-inline-delete-response.html",
                {"name": name},
            )
        return redirect(success_url)
    context = {"object": obj}
    return render(request, "recipes/delete.html", context)


@login_required
def recipe_detail_hx_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except Exception as e:
        print(e)
        obj = None
    if obj is None:
        return HttpResponse("Não encontrado")
    context = {"object": obj}
    return render(request, "recipes/partials/detail.html", context)


@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.active = True
        obj.save()
        if request.htmx:
            headers = {"HX-Redirect": obj.get_absolute_url()}
            return HttpResponse("Criado", headers=headers)
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create-update.html", context)


@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    new_ingredient_url = reverse(
        "recipes:ingredient_create_hx", kwargs={"parent_id": obj.id}
    )
    context = {
        "form": form,
        "object": obj,
        "new_ingredient_url": new_ingredient_url,
    }
    if form.is_valid():
        form.save()
        context["message"] = "Atualizado com sucesso!"
    if request.htmx:
        return render(request, "recipes/partials/forms.html", context)
    return render(request, "recipes/create-update.html", context)


@login_required
def recipe_ingredient_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except Exception as e:
        print(e)
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Não encontrado")

    instance = None

    if id is not None:
        try:
            instance = RecipeIngredient.objects.get(recipe=parent_obj, id=id)
        except Exception as e:
            print(e)
            instance = None
    form = RecipeIngredientForm(request.POST or None, instance=instance)
    url = reverse(
        "recipes:ingredient_create_hx", kwargs={"parent_id": parent_obj.id}
    )
    if instance:
        url = instance.get_hx_edit_url()

    context = {"object": instance, "form": form, "url": url}
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context["object"] = new_obj
        return render(
            request, "recipes/partials/ingredient-inline.html", context
        )
    return render(request, "recipes/partials/ingredient-form.html", context)


def recipe_ingredient_image_upload_view(request, parent_id=None):
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except Exception as e:
        print(e)
        parent_obj = None
    if parent_obj is None:
        raise Http404
    form = RecipeIngredientImageForm(
        request.POST or None, request.FILES or None
    )
    if form.is_valid():
        obj = form.save(commit=False)
        obj.recipe = parent_obj
        obj.save()
    return render(request, "image-form.html", {"form": form})
