from django.contrib import admin
from django.urls import path, include
from Users import views as userViews
from django.contrib.auth import views as authViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('FreelanceExchange.urls')),
    path('api/v2/', include('Users.urls'), name="profile"),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
