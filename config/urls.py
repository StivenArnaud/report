from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('reporting/', include('reporting.urls')),
    path('pointing/', include('pointing.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = 'core.views.error400'
handler403 = 'core.views.error403'
handler404 = 'core.views.error404'
handler500 = 'core.views.error500'
