from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Goal


@api_view(['POST'])
def views(request):
    if request.method == 'POST':
        return create(request)


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
