from articles.models import Article
from django.shortcuts import render
from recipes.models import Recipe

SEARCH_TYPE_MAPPING = {
    "articles": Article,
    "article": Article,
    "recipes": Recipe,
    "recipe": Recipe,
}


def search_view(request):
    query = request.GET.get("q")
    search_type = request.GET.get("type")
    Klass = Recipe
    if search_type in SEARCH_TYPE_MAPPING.keys():
        Klass = SEARCH_TYPE_MAPPING[search_type]
    qs = Klass.objects.search(query=query)
    context = {"queryset": qs}
    template = "search/results-views.html"
    if request.htmx:
        context["queryset"] = qs[:5]
        template = "search/partials/results.html"
    return render(request, template, context)
