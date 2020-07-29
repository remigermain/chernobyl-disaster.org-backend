from .views import TagViewSet, TagLangViewSet, PeopleViewSet, ContactViewSet, \
    IssueViewSet

drf_routers = (
    ('tag', TagViewSet),
    ('tag/lang', TagLangViewSet),
    ('people', PeopleViewSet),
    ('contact', ContactViewSet),
    ('issue', IssueViewSet),
)
