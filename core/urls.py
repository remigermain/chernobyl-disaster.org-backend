from django.contrib import admin
from django.urls import path, include
from common import urls as common_urls
from timeline import urls as timeline_urls
from gallery import urls as gallery_urls
from utils import urls as utils_urls
from rest_framework import routers
from django.contrib.staticfiles.urls import static
from django.conf import settings
import os


router = routers.DefaultRouter()
# load the url of all app
urls = [
    *common_urls.drf_routers,
    *timeline_urls.drf_routers,
    *gallery_urls.drf_routers,
    *utils_urls.drf_routers
]
for url in urls:
    router.register(*url)


urlpatterns = [
    # api models
    path('', include(router.urls)),
    path('populate/', include('populate.urls'), name="populate"),

    # account / auth
    path('auth/', include('authentication.urls')),
]


if settings.DEBUG:

    urlpatterns.append(path('admin/', admin.site.urls))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if settings.DEBUG_TOOLBAR:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# for produdction
else:

    # add admin django only if sufffix_admin is set and min length 8 char
    SUFFIX_ADMIN = os.environ.get("SUFFIX_ADMIN", None)
    if SUFFIX_ADMIN and len(SUFFIX_ADMIN) >= 8:
        urlpatterns.append(path(f'admin-{SUFFIX_ADMIN}/', admin.site.urls))
