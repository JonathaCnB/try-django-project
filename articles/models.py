from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from django.utils import timezone

from .utils import slugify_instance_title


class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Article(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    publish = models.DateField(
        auto_now_add=False, auto_now=False, default=timezone.now
    )

    objects = ArticleManager()

    @property
    def name(self):
        return self.title

    class Meta:
        db_table = "article_article"

    def get_absolute_url(self):
        return reverse("articles:detail_view", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.id} | {self.title}"


def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)


pre_save.connect(article_pre_save, sender=Article)


def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)


post_save.connect(article_post_save, sender=Article)
