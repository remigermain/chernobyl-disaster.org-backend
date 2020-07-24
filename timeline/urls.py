from django.urls import path, include
from rest_framework import routers
from timeline import views

# restframework url router
router = routers.DefaultRouter()

# router.register('picture/lang', views.EventLangViewSet)
router.register('picture', views.PictureViewSet)

# router.register('document/lang', views.EventLangViewSet)
router.register('document', views.DocumentViewSet)

# router.register('article/lang', views.EventLangViewSet)
router.register('article', views.ArticleViewSet)

# router.register('video/lang', views.EventLangViewSet)
router.register('video', views.VideoViewSet)

router.register('lang', views.EventLangViewSet)
router.register('', views.EventViewSet)


urlpatterns = [
    path('/', include(router.urls)),
]
