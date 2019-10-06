from tasks import models as task_models


def is_upgrade(status_current, status_next):
    if status_current == 'not_started':
        return status_next in ['in_progress', 'completed']
    if status_current == 'in_progress':
        return status_next in ['completed']
    return False


def get_parent(t):
    try:
        return Task.objects.get(id=t.parent_id)
    except:
        return None


def get_siblings(t):
    if not get_parent(t):
        return task_models.Task.objects.none()
    return get_parent(t).get_subtasks().exclude(id=t.id).order_by('-created')
