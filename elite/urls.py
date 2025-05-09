from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from index.views import custom_404, custom_500, serve_media
import os

urlpatterns = [
    path('elite/admin/', admin.site.urls),
    path('elite/', include('index.urls')), 
    path('i18n/', include('django.conf.urls.i18n')), 
]

handler404 = 'index.views.custom_404'
handler500 = 'index.views.custom_500'

# Development: Serve media and static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Production: Secure media serving
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve_media),
    ]
