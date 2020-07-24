from .views import TagViewSet, TagLangViewSet, PeopleViewSet

drf_routers = (
    ('tag', TagViewSet),
    ('tag/lang', TagLangViewSet),
    ('people', PeopleViewSet),
)
