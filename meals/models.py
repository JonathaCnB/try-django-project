from django.db import models
from recipes.models import Recipe
from users.models import User


class MealStatus(models.TextChoices):
    PENDING = "p", "Pendente"
    COMPLETED = "c", "Completo"
    EXPIRED = "e", "Expirado"
    ABORTED = "a", "Abortado"


class MealQuerySet(models.QuerySet):
    def by_user_id(self, user_id):
        return self.filter(user_id=user_id)

    def by_user(self, user):
        return self.filter(user=user)

    def pending(self):
        return self.filter(status=MealStatus.PENDING)

    def completed(self):
        return self.filter(status=MealStatus.COMPLETED)

    def expired(self):
        return self.filter(status=MealStatus.EXPIRED)

    def aborted(self):
        return self.filter(status=MealStatus.ABORTED)

    def in_queue(self, recipe_id):
        return self.pending().filter(recipe_id=recipe_id)


class MealManager(models.Manager):
    def get_queryset(self):
        return MealQuerySet(self.model, using=self._db)

    def by_user_id(self, user_id):
        return self.get_queryset().by_user_id(user_id)

    def by_user(self, user):
        return self.get_queryset().by_user(user)

    def toggle_in_queue(self, user_id, recipe_id):
        qs = self.get_queryset().all().by_user_id(user_id)
        already_queued = qs.in_queue(recipe_id)
        added = None
        if already_queued:
            recipe_qs = qs.filter(recipe_id=recipe_id)
            recipe_qs.update(status=MealStatus.ABORTED)
            added = False
        else:
            obj = self.model(
                user_id=user_id, recipe_id=recipe_id, status=MealStatus.PENDING
            )
            obj.save()
            added = True
        return added


class Meal(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=1,
        choices=MealStatus.choices,
        default=MealStatus.PENDING,
    )
    active = models.BooleanField(default=True)

    objects = MealManager()
