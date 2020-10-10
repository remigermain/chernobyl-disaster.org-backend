from common import views

drf_routers = (
    ('tag', views.TagViewSet),
    ('tag-lang', views.TagLangViewSet),
    ('translate', views.TranslateViewSet),
    ('translatelang', views.TranslateLangViewSet),
)
