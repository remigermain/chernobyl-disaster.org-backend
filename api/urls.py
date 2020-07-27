from django.urls import path, include, re_path

app_name = "api"

urlpatterns = [
    # auth api
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),

]
