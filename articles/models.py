from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        db_table = "article_article"

    def __str__(self):
        return f'{self.id} | {self.title}'
