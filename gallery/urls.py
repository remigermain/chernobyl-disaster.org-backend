from gallery import views

drf_routers = [
    ('character', views.CharacterViewSet),
    ('character-lang', views.CharacterLangViewSet),
    ('picture', views.PictureViewSet),
    ('picture-lang', views.PictureLangViewSet),
    ('video', views.VideoViewSet),
    ('video-lang', views.VideoLangViewSet),
]
