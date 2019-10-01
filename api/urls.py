from django.urls import path
from goals import views as goals_views


app_name = 'api'

urlpatterns = [
    path(
        'goals/',
        goals_views.views,
        name='goals-create-list',
    ),
]
