from .views import TagViewSet, TagLangViewSet, PeopleViewSet, ContactViewSet, \
    IssueViewSet, PeopleLangViewSet

drf_routers = (
    ('tag', TagViewSet),
    ('tag/lang', TagLangViewSet),
    ('people', PeopleViewSet),
    ('people/lang', PeopleLangViewSet),
    ('contact', ContactViewSet),
    ('issue', IssueViewSet),
)
