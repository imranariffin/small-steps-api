import uuid

from django.db import models
from django.utils import timezone


class Account(models.Model):
    created = models.DateTimeField(
        default=timezone.now,
    )
    device_id = models.CharField(
        blank=False,
        max_length=256,
        null=False,
        unique=True,
    )
    id = models.UUIDField(
        blank=False,
        default=uuid.uuid4,
        editable=False,
        null=False,
        primary_key=True,
    )
