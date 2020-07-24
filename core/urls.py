from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('timeline', include('timeline.urls')),
    path('admin/', admin.site.urls),
]
