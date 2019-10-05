from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from tasks.models import Task
from tasks.exceptions import ParentDoesNotExist


@api_view(['POST', 'GET'])
@renderer_classes([JSONRenderer])
def views(request):
    if request.method == 'POST':
        return tasks_create(request)

    if request.method == 'GET':
        return tasks_list(request)


def tasks_create(request):
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
        task = Task.objects.create(parent_id=parent_id, text=text)
    except ParentDoesNotExist:
        return Response(
            {
                'parent_id': f'Parent with id {parent_id} does not exist',
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            'created': task.created,
            'id': task.id,
            'parent_id': parent_id,
            'text': text,
        },
        status=status.HTTP_201_CREATED,
    )


def tasks_list(request):
    return Response(
        {
            'tasks': list(map(
                lambda task: (
                    {
                        'id': task.id,
                        'created': task.created,
                        'parent_id': task.parent_id,
                    }
                ),
                Task.objects.all().order_by('-created'),
            ))
        },
        status=status.HTTP_200_OK,
    )
