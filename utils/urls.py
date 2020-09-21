from utils.views import ContactViewSet, IssueViewSet

drf_routers = (
    ('contact', ContactViewSet),
    ('issue', IssueViewSet)
)
