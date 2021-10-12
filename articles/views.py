import random

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
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
        "name": name,
    }
    # Django Templates
    HTML_STRING = render_to_string("home-view.html", context=context)
    # HTML_STRING = """
    # <h1>{title} (id: {id})!</h1>
    # <p>{content}!</p>
    # """.format(**context)
    return HttpResponse(HTML_STRING)


def article_search_view(request):
    query = request.GET.get("q")
    qs = Article.objects.search(query=query)
    context = {"object_list": qs}
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
        return redirect(obj.get_absolute_url())

    return render(request, "articles/create.html", context)


def article_detail_view(request, slug=None):
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
        except Exception as e:
            print(e)
            raise Http404

    context = {
        "object": article_obj,
    }

    return render(request, "articles/detail.html", context)
