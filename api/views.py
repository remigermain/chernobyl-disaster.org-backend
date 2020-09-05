from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['POST', 'delete'])
def deleteAcount(request):
    user = request.user
    user.is_active = False
    user.save()
    return response(status=status.HTTP_200_OK)
