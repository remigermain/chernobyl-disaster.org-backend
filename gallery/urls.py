from gallery.views import VideoViewSet, PeopleViewSet, PictureViewSet

drf_routers = [
    ('people', PeopleViewSet),
    ('picture', PictureViewSet),
    ('video', VideoViewSet),
]