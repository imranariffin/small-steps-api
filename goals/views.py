from rest_framework import status
from rest_framework.decorators import (
    api_view,
    parser_classes,
    renderer_classes
)
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import Goal, GoalDeleted


@api_view(['POST', 'GET', 'DELETE'])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def views(request, goal_id=None):
    if request.method == 'POST':
        return goals_create(request)

    elif request.method == 'GET':
        return goals_list(request)

    elif request.method == 'DELETE':
        return goals_delete(request, goal_id)


def goals_create(request):
    text = request.data['text']
    goal = Goal.objects.create(text=text)
    return Response(
        {
            'created': goal.created,
            'id': goal.id,
            'text': goal.text,
        },
        status=status.HTTP_201_CREATED,
    )


def goals_list(request):
    return Response(
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
        return Response(
            {
                'goal_id': f'Goal with id {goal_id} not found',
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    goal.delete()
    datetime_deleted = GoalDeleted.objects.get(goal=goal.id).created

    return Response(
        {
           'id': str(goal_id),
           'datetime_deleted': datetime_deleted,
        },
        status=status.HTTP_200_OK,
    )
