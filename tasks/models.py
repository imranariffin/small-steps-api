import uuid

from django.db import models, utils
from django.utils import timezone

from goals.models import Goal
from tasks.exceptions import ParentDoesNotExist


class Task(models.Model):
    created = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(
        blank=False,
        default=uuid.uuid4,
        null=False,
        primary_key=True,
    )
    parent_id = models.UUIDField(
        blank=False,
        null=False,
        primary_key=False,
    )
    text = models.CharField(
        blank=True,
        default=None,
        max_length=200,
        null=False,
    )

    def save(self, *args, **kwargs):
        try:
            Goal.objects.get(id=self.parent_id)
        except Goal.DoesNotExist:
            try:
                Task.objects.get(id=self.parent_id)
            except Task.DoesNotExist:
                raise ParentDoesNotExist(
                    f'Parent with id {self.parent_id} does not exist'
                )

        super().save(*args, **kwargs)
