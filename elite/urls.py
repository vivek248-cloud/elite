from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from index.views import custom_404, custom_500, serve_media

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
]

# Custom error handlers
handler404 = 'index.views.custom_404'
handler500 = 'index.views.custom_500'

# Development static and media serving
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
else:
    # Media serving fallback in production (not recommended)
    urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve_media)]
