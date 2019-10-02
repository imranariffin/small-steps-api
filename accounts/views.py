from django.http import JsonResponse
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view

from accounts.models import Account


@api_view(['POST'])
def views(request):
    device_id = request.POST['device_id']
    account = None

    try:
        account = Account.objects.create(device_id=device_id)
    except IntegrityError:
        return JsonResponse(
            {
                'device_id': (
                    'Device id some-existing-device-id '
                    'already exists'
                ),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    return JsonResponse(
        {
            'created': account.created,
            'id': account.id,
        },
        status=status.HTTP_201_CREATED,
    )
