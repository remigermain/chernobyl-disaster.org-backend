from .views import TagViewSet, TranslateViewSet, TranslateLangViewSet

drf_routers = (
    ('tag', TagViewSet),
    # ('tag/lang', TagLangViewSet),
    # ('people/lang', PeopleLangViewSet),
    ('translate', TranslateViewSet),
    ('translatelang', TranslateLangViewSet),
)
