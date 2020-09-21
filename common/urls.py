from .views import TagViewSet, ContactViewSet, \
    IssueViewSet, TranslateViewSet, TranslateLangViewSet

drf_routers = (
    ('tag', TagViewSet),
    # ('tag/lang', TagLangViewSet),
    # ('people/lang', PeopleLangViewSet),
    ('contact', ContactViewSet),
    ('issue', IssueViewSet),
    ('translate', TranslateViewSet),
    ('translatelang', TranslateLangViewSet),
)
