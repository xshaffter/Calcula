from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from api.urls import url_patterns as api_urls
from main import urls as main_urls
from cat.urls import url_patterns as cat_urls
urlpatterns = [
    path('api/', include(api_urls)),
    path('cat/', include((cat_urls, 'cat'), namespace='cat')),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include((main_urls, 'main'), namespace='app')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
