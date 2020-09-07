from rest_framework.response import responses
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK


@api_view(['POST', 'delete'])
def deleteAcount(request):
    user = request.user
    user.is_active = False
    user.save()
    return responses(status=HTTP_200_OK)
