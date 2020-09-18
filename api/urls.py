from django.urls import path, include, re_path
from api.views import deleteAcount, PasswordReset, VerifyEmail
from django.views.generic import TemplateView


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^registration/confirm-email/(?P<key>[-:\w]+)/$', VerifyEmail.as_view(), name='account_confirm_email'),
    path('registration/verify-email/', TemplateView.as_view(), name='account_email_verification_sent'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordReset.as_view(), name='password_reset_confirm'),
    path('delete/', deleteAcount),
]
