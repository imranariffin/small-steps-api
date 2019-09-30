from django.http import JsonResponse
from rest_framework import status

from .models import Goal


def create(request):
    text = request.POST['text']
    goal = Goal.objects.create(text=text)
    return JsonResponse(
        {
            'created': goal.created,
            'id': str(goal.id),
            'text': goal.text,
        },
        status=status.HTTP_201_CREATED,
    )
