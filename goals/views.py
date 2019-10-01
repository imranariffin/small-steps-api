from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Goal


@api_view(['POST', 'GET'])
def views(request):
    if request.method == 'POST':
        return goals_create(request)

    elif request.method == 'GET':
        return goals_list(request)


def goals_create(request):
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


def goals_list(request):
    return JsonResponse(
        {
            'goals': list(map(
                lambda goal: (
                    {
                        'created': goal.created,
                        'id': str(goal.id),
                        'text': goal.text,
                    }
                ),
                list(Goal.objects.all().order_by('-created'))
            )),
        },
        status=status.HTTP_200_OK,
    )
