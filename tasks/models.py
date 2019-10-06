import uuid

from django.db import models
from django.utils import timezone

from goals.models import Goal
from tasks.exceptions import ParentDoesNotExist
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
            Goal.objects.get(id=self.parent_id)
        except Goal.DoesNotExist:
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
        except:
            return None

    def get_siblings(self):
        parent = self.get_parent()

        if not parent:
            return Task.objects.none()

        return Task.objects\
            .filter(parent_id=parent.id)\
            .exclude(id=self.id)\
            .order_by('-created')

    def get_subtasks(self):
        return Task.objects.filter(parent_id=self.id).order_by('-created')

    def transition_to(self, status_next):
        self.status = status_next

        for subtask in Task.objects.filter(parent_id=self.id):
            subtask.transition_to(status_next)

        if all(map(
                lambda t: t.status == status_next and utils.is_upgrade(t.status, status_next),
                self.get_siblings(),
        )):
            if self.get_parent():
                self.get_parent().transition_to(status_next)

        self.save()
