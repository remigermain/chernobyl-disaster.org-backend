from django.urls import path, include
from populate import views

translate = [
    path('overview', views.translate_overview),
    path('upload', views.translate_json),
    path('delete/<str:lang>/', views.translate_delete),
]

urlpatterns = [
    path('store', views.populate),
    path('picture', views.picture),
    path('people', views.people),
    path('overview', views.overview),
    path('contributors', views.contributor),
    path('translate/', include(translate))
]
