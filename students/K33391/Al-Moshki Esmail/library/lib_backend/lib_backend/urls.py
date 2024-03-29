from django.contrib import admin
from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
    path('login/', login),
    path('signup/', signup),
    path('test_token/', test_token),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]
