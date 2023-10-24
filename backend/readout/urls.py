from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include("user_app.urls")),
    path('api/v1/prefs/', include("pref_app.urls")),
]
