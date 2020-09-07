from timeline import views

drf_routers = (
    ('picture/lang', views.PictureLangViewSet),
    ('picture', views.PictureViewSet),

    ('video/lang', views.VideoLangViewSet),
    ('video', views.VideoViewSet),

    ('event/lang', views.EventLangViewSet),
    ('event', views.EventViewSet),
)
