from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['POST'])
def views(request):
    return JsonResponse({}, status=status.HTTP_201_CREATED)
