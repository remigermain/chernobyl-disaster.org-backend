from .views import TagViewSet, TranslateViewSet, TranslateLangViewSet

drf_routers = (
    ('tag', TagViewSet),
    ('translate', TranslateViewSet),
    ('translatelang', TranslateLangViewSet),
)
