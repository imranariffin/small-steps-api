from django.contrib import admin
from django.http import JsonResponse
from django.urls import path


urlpatterns = [
    path('', lambda _: JsonResponse({'message': 'Hello, world'})),
    path('admin/', admin.site.urls),
]
