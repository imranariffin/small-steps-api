from uuid import UUID

from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from goals.models import Goal
from tasks.models import Task


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def views(request):
    try:
        text = request.data['text']
        parent_id = request.data['parent_id']
    except KeyError as ex:
        return Response(
            {
                ex.args[0]: 'This field is required',
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        Goal.objects.get(id=UUID(parent_id))
    except Goal.DoesNotExist:
        try:
            Task.objects.get(id=UUID(parent_id))
        except Task.DoesNotExist:
            return Response(
                {
                    'parent_id': f'Parent with id {parent_id} does not exist',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    task = Task.objects.create()

    return Response(
        {
            'created': task.created,
            'id': task.id,
            'parent_id': parent_id,
            'text': text,
        },
        status=status.HTTP_201_CREATED,
    )
