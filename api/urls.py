from django.urls import path

from accounts import views as accounts_views
from goals import views as goals_views
from tasks import views as tasks_views


app_name = 'api'

urlpatterns = [
    path(
        'accounts/',
        accounts_views.views,
        name='accounts-create',
    ),
    path(
        'goals/',
        goals_views.views,
        name='goals-create-list',
    ),
    path(
        'goals/<uuid:goal_id>/',
        goals_views.views,
        name='goals-delete',
    ),
    path(
        'tasks/',
        tasks_views.views,
        name='tasks-create-list',
    ),
    path(
        'tasks/<uuid:task_id>/status/',
        tasks_views.views_status,
        name='tasks-status-update',
    ),
]
