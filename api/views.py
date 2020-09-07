from rest_framework.response import responses
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['POST', 'delete'])
def deleteAcount(request):
    user = request.user
    user.is_active = False
    user.save()
    return responses(status=status.HTTP_200_OK)
