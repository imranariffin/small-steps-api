from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    parser_classes,
    renderer_classes
)
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from accounts.models import Account


@api_view(['POST'])
@parser_classes([JSONParser])
@renderer_classes([JSONRenderer])
def views(request):
    device_id = request.data['device_id']
    account = None

    try:
        account = Account.objects.create(device_id=device_id)
    except IntegrityError:
        return Response(
            {
                'device_id': (
                    'Device id some-existing-device-id '
                    'already exists'
                ),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            'created': account.created,
            'id': account.id,
        },
        status=status.HTTP_201_CREATED,
    )
