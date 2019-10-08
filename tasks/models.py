import uuid

from django.db import models
from django.utils import timezone

from goals import models as goals_models
from tasks.exceptions import (
    ParentDoesNotExist,
    InvalidStatusTransition
)
from tasks import choices


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
    status = models.CharField(
        blank=False,
        choices=choices.TASKS_STATUSES,
        default=choices.NOT_STARTED,
        max_length=200,
        null=False,
    )

    def save(self, *args, **kwargs):
        try:
            goals_models.Goal.objects.get(id=self.parent_id)
        except goals_models.Goal.DoesNotExist:
            try:
                Task.objects.get(id=self.parent_id)
            except Task.DoesNotExist:
                raise ParentDoesNotExist(
                    f'Parent with id {self.parent_id} does not exist'
                )
        self.clean_fields()
        super().save(*args, **kwargs)

    def get_parent(self):
        try:
            return Task.objects.get(id=self.parent_id)
        except Task.DoesNotExist:
            return goals_models.Goal.objects.get(id=self.parent_id)

    def get_siblings(self):
        parent = self.get_parent()

        if not parent:
            return Task.objects.none()

        ret = Task.objects\
            .filter(parent_id=parent.id)\
            .exclude(id=self.id)\
            .order_by('-created')
        return ret

    def get_subtasks(self):
        return Task.objects.filter(parent_id=self.id).order_by('-created')

    def has_subtasks(self):
        return len(self.get_subtasks()) > 0

    def transition_to(self, status_next):
        if self.has_subtasks():
            raise InvalidStatusTransition

        if self.status == 'not_started' and status_next == 'completed':
            raise InvalidStatusTransition

        status = self.status
        if (
                status == 'not_started' and status_next == 'in_progress' or
                status == 'in_progress' and status_next == 'completed' or
                status == 'completed' and status_next == 'in_progress' or
                status == 'in_progress' and status_next == 'not_started'
        ):
            self._transition_to(status_next)

    def _transition_to(self, status_next, transition_parent=False):
        should_parent_transition = self._should_parent_transition(status_next)

        if should_parent_transition:
            self.get_parent()._transition_to(status_next)

        self.status = status_next
        self.save()

    def _should_parent_transition(self, status_next):
        if status_next == 'in_progress':
            return self.get_parent().status != 'in_progress'

        return all(
            map(
                lambda s: s.status == status_next,
                self.get_siblings(),
            ),
        )
