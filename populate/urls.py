from django.urls import path, include
from populate import views

translate = [
    path('overview', views.translate_overview),
    path('upload', views.translate_json),
    path('delete/<str:lang>/', views.translate_delete),
]

urlpatterns = [
    path('store', views.PopulateView.as_view()),
    path('picture', views.PictureView.as_view()),
    path('people', views.PeopleView.as_view()),
    path('overview', views.OverView.as_view()),
    path('contributors', views.ContributorView.as_view()),
    path('translate/', include(translate))
]
