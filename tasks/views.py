from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from tasks.models import Task


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def views(request):
    text = request.data['text']
    parent_id = request.data['parent_id']

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
