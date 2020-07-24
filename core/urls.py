from django.contrib import admin
from django.urls import path, include
from common.urls import drf_routers as common_urls
from timeline.urls import drf_routers as timeline_urls
from rest_framework import routers

router = routers.DefaultRouter()

for r in common_urls:
    router.register(*r)

for r in timeline_urls:
    router.register(*r)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
