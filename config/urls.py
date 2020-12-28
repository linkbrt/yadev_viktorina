from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static

from config import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',
         include('users.urls')),
    path('auth/',
         include('django.contrib.auth.urls')),
    path('', include('quiz.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # noqa
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # noqa
