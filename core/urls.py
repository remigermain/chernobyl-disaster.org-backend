from django.contrib import admin
from django.urls import path, include, re_path
from common.urls import drf_routers as common_urls
from timeline.urls import drf_routers as timeline_urls
from rest_framework import routers
from dj_rest_auth.registration.views import VerifyEmailView


router = routers.DefaultRouter()

# load the url of all app
apps = [
    common_urls,
    timeline_urls
]

# register all urls in all apps
for app in apps:
    for url in app:
        router.register(*url)

urlpatterns = [
    # api models
    path('', include(router.urls)),

    # account / auth
    path('auth/', include('api.urls')),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),

    # admin
    path('admin/', admin.site.urls),
]
