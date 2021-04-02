from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path


handler404 = 'recipes.views.page_not_found'
handler500 = 'recipes.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('recipes.urls')),
    path(
        'about-project/', views.flatpage,
        {'url': '/about-project/'}, name='about-project'),
    path(
        'about-author/', views.flatpage,
        {'url': '/about-author/'}, name='about-author'),
    path(
        'about-spec/', views.flatpage,
        {'url': '/about-spec/'}, name='about-spec'),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
