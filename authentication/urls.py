from django.urls import path, include, re_path
from authentication.views import deleteAcount, PasswordReset, VerifyEmail


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^registration/verify-email/(?P<key>[-:\w]+)/$', VerifyEmail.as_view(), name='account_confirm_email'),
    path('registration/verify-email/', VerifyEmail.as_view(), name='account_email_verification_sent'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordReset.as_view(), name='password_reset_confirm'),
    path('delete/', deleteAcount),
]
