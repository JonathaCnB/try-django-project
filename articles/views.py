import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from articles.models import Article

from .forms import ArticleForms


def homepage(request, *args, **kwargs):
    name = "Jonatha"  # Hard Code
    random_id = random.randint(1, 4)  # pseudo random

    # from the database??
    article_obj = Article.objects.get(id=random_id)
    article_queryset = Article.objects.all()
    context = {
        "object_list": article_queryset,
        "object": article_obj,
        "title": article_obj.title,
        "id": article_obj.id,
        "content": article_obj.content,
    }
    # Django Templates
    HTML_STRING = render_to_string("home-view.html", context=context)
    # HTML_STRING = """
    # <h1>{title} (id: {id})!</h1>
    # <p>{content}!</p>
    # """.format(**context)
    return HttpResponse(HTML_STRING)


def article_search_view(request):
    query_dict = request.GET
    try:
        query = int(query_dict.get("q"))
    except:
        query = None

    article_obj = None
    if query is not None:
        article_obj = Article.objects.get(id=query)
    context = {"object": article_obj}
    return render(request, "articles/search.html", context)


@login_required
def article_create_view(request, id=None):
    form = ArticleForms(request.POST or None)
    context = {"created": False, "form": form}

    if form.is_valid():
        obj = form.save()
        # title = request.POST.get("title")
        # content = request.POST.get("content")
        # obj = Article.objects.create(title=title, content=content)
        context["object"] = obj
        context["created"] = True

    return render(request, "articles/create.html", context)


def article_detail_view(request, id=None):
    article_obj = None
    if id is not None:
        article_obj = Article.objects.get(id=id)

    context = {
        "object": article_obj,
    }

    return render(request, "articles/detail.html", context)
