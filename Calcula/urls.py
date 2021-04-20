from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from main import urls as main_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(main_urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
