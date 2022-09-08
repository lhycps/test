from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from crm import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('system.urls')),
    path('djcp/', include('djcp.urls')),
    path('sale/', include('sales.urls')),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
