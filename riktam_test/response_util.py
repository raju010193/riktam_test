from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


def response_format(**kwargs):
    data = {
        "message": kwargs.get('message', None),
        "error": kwargs.get('error', None),
        "is_success": kwargs.get('is_success', True),
        "status": kwargs.get('status', 200),
        "data": kwargs.get('data', None)
    }
    return Response(data, status=kwargs.get('status'))
