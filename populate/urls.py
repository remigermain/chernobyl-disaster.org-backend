from django.urls import path
from populate import views

urlpatterns = [
    path('store', views.PopulateView.as_view()),
    path('picture', views.PictureView.as_view()),
    path('people', views.PeopleView.as_view()),
    path('overview', views.OverView.as_view()),
    path('contributors', views.ContributorView.as_view()),
]