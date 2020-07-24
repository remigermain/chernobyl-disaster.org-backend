from timeline import views

drf_routers = (
    ('picture/lang', views.PictureLangViewSet),
    ('picture', views.PictureViewSet),

    ('document/lang', views.DocumentLangViewSet),
    ('document', views.DocumentViewSet),

    ('article/lang', views.ArticleLangViewSet),
    ('article', views.ArticleViewSet),

    ('video/lang', views.VideoLangViewSet),
    ('video', views.VideoViewSet),

    ('event/lang', views.EventLangViewSet),
    ('event', views.EventViewSet),
)
