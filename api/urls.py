from django.urls import path
from goals import views as goals_views
from accounts import views as accounts_views


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
]
