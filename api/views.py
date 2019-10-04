from django.http import JsonResponse
from rest_framework import status


def create(request):
    return JsonResponse(
        {
            'message': 'Hello, world'
        },
        status=status.HTTP_201_CREATED,
    )
