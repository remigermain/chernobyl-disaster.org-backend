from django.contrib import admin
from django.urls import path, include
from common import urls as common_urls
from timeline import urls as timeline_urls
from gallery import urls as gallery_urls
from rest_framework import routers
from django.contrib.staticfiles.urls import static
from django.conf import settings


router = routers.DefaultRouter()
# load the url of all app
apps = [
    common_urls,
    timeline_urls,
    gallery_urls
]
for app in apps:
    for url in app.drf_routers:
        router.register(*url)

urlpatterns = [
    # api models
    path('', include(router.urls)),
    path('populate/', include('populate.urls'), name="populate"),

    # account / auth
    path('auth/', include('authentication.urls')),

    # admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
