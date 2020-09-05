from django.urls import path, include
from api.views import deleteAcount

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('delete/', deleteAcount),
]
