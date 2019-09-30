from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path(
        'goals/',
        views.create,
        name='goals-create',
    ),
]
