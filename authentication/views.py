from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordResetConfirmView
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST', 'delete'])
@permission_classes([IsAuthenticated])
def deleteAcount(request):
    user = request.user
    user.delete()
    return Response(status=HTTP_200_OK)


class PasswordReset(PasswordResetConfirmView):
    """
        view for password reset in frontend , not backend
    """
    def get(self, *args, **kwargs):
        query = f"uid={kwargs['uidb64']}&token={kwargs['token']}"
        return redirect(f"{settings.FRONTEND_URL}/auth/change-password/?{query}")


class VerifyEmail(VerifyEmailView):
    """
        view for verify email in frontend , not backend
    """
    def get(self, *args, **kwargs):
        query = f"key={kwargs['key']}"
        return redirect(f"{settings.FRONTEND_URL}/auth/verify-email/?{query}")
