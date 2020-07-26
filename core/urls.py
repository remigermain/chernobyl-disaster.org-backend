from django.contrib import admin
from django.urls import path, include
from common.urls import drf_routers as common_urls
from timeline.urls import drf_routers as timeline_urls
from rest_framework import routers

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

    # auth api
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),

    # admin
    path('admin/', admin.site.urls),
]
