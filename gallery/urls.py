from gallery import views

drf_routers = [
    ('people', views.PeopleViewSet),
    ('people-lang', views.PeopleLangViewSet),
    ('picture', views.PictureViewSet),
    ('picture-lang', views.PictureLangViewSet),
    ('video', views.VideoViewSet),
    ('video-lang', views.VideoLangViewSet),
]
