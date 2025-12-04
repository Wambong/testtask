

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'orders.views.custom_403'

