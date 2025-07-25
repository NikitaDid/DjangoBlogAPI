"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings

# Connecting all urls from whole project
urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('apps.blog.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('user/', include('apps.user.urls')),
    path('order/', include('apps.order.urls')),
    path('api/', include('apps.api.urls')),
    path('', include('apps.main.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




