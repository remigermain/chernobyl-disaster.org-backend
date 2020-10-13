from common import views

drf_routers = (
    ('news', views.NewsViewSet),
    ('tag', views.TagViewSet),
    ('tag-lang', views.TagLangViewSet),
    ('translate', views.TranslateViewSet),
    ('translatelang', views.TranslateLangViewSet),
)
