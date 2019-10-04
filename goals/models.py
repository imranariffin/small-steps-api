import uuid

from django.db import models
from django.utils import timezone


class Goal(models.Model):
    created = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(
        blank=False,
        default=uuid.uuid4,
        editable=False,
        null=False,
        primary_key=True,
    )
    text = models.CharField(max_length=200)

    def _mark_delete(self):
        GoalDeleted.objects.create(goal=self)

    def delete(self):
        self._mark_delete()


class GoalDeleted(models.Model):
    created = models.DateTimeField(default=timezone.now)
    goal = models.OneToOneField(
        'Goal',
        on_delete=models.CASCADE,
        primary_key=True,
    )
