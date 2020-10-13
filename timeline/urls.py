from timeline import views

drf_routers = (
    ('event', views.EventViewSet),
    ('event-lang', views.EventLangViewSet)
)
