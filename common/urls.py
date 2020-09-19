from .views import TagViewSet, PeopleViewSet, ContactViewSet, \
    IssueViewSet, TranslateViewSet, TranslateLangViewSet

drf_routers = (
    ('tag', TagViewSet),
    # ('tag/lang', TagLangViewSet),
    ('people', PeopleViewSet),
    # ('people/lang', PeopleLangViewSet),
    ('contact', ContactViewSet),
    ('issue', IssueViewSet),
    ('translate', TranslateViewSet),
    ('translatelang', TranslateLangViewSet),
)
