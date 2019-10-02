from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Goal


@api_view(['POST', 'GET', 'DELETE'])
def views(request, goal_id=None):
    if request.method == 'POST':
        return goals_create(request)

    elif request.method == 'GET':
        return goals_list(request)

    elif request.method == 'DELETE':
        return goals_delete(request, goal_id)


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


def goals_delete(request, goal_id):
    goal = None
    try:
        goal = Goal.objects.get(pk=goal_id)
    except Goal.DoesNotExist:
        return JsonResponse(
            {
                'goal_id': f'Goal with id {goal_id} not found',
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    goal.delete()

    return JsonResponse(
        {
           'id': str(goal.id),
        },
        status=status.HTTP_200_OK,
    )
