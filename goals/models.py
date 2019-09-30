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
