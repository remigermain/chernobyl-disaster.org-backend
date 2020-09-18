from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordResetConfirmView
from django.shortcuts import redirect
from django.conf import settings


@api_view(['POST', 'delete'])
def deleteAcount(request):
    user = request.user
    user.is_active = False
    # user.delete()
    user.save()
    return Response(status=HTTP_200_OK)


class PasswordReset(PasswordResetConfirmView):
    def get(self, *args, **kwargs):
        query = f"uid={kwargs['uidb64']}&token={kwargs['token']}"
        return redirect(f"{settings.FRONTEND_URL}/auth/change-password/?{query}")


class VerifyEmail(VerifyEmailView):
    def get(self, *args, **kwargs):
        query = f"key={kwargs['key']}"
        return redirect(f"{settings.FRONTEND_URL}/auth/verify-email/?{query}")
