import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, IntegrityError
from django.utils import timezone

from goals.models import Goal


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

    def save(self, *args, **kwargs):
        try:
            Goal.objects.get(id=self.parent_id)
        except Goal.DoesNotExist:
            try:
                Task.objects.get(id=self.parent_id)
            except Task.DoesNotExist:
                raise IntegrityError(
                    f'Parent with id {self.parent_id} does not exist'
                )
        
        super().save(*args, **kwargs)
