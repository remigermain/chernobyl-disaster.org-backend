from django.urls import path, include
from populate import views

translate = [
    path('overview', views.translate_overview, name="translate_overview"),
    path('upload', views.translate_json, name="translate_upload"),
    path('delete/<str:lang>/', views.translate_delete, name="translate_delete"),
]

urlpatterns = [
    path('store', views.populate, name="populate_store"),
    path('character', views.character, name="populate_character"),
    path('overview', views.overview, name="populate_overview"),
    path('contributors', views.contributor, name="populate_contributors"),
    path('translate/', include(translate))
]
