import uuid

from django.db import models
from django.utils import timezone

from tasks import (
    choices as tasks_status_choices,
    models as tasks_models
)


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
    status = models.CharField(
        blank=False,
        choices=tasks_status_choices.TASKS_STATUSES,
        default=tasks_status_choices.NOT_STARTED,
        max_length=200,
        null=False,
    )

    def _mark_delete(self):
        GoalDeleted.objects.create(goal=self)

    def delete(self):
        self._mark_delete()

    def get_tasks(self):
        return tasks_models.Task.objects.filter(parent_id=self.id)

    def _transition_to(self, status_next, transition_parent=False):
        self.status = status_next
        self.save()


class GoalDeleted(models.Model):
    created = models.DateTimeField(default=timezone.now)
    goal = models.OneToOneField(
        'Goal',
        on_delete=models.CASCADE,
        primary_key=True,
    )
