"""ticketsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

### IMPORT THE APPLICABLE SETTINGS SET IN manage.py ###
from manage import USED_SETTINGS

import importlib
used_settings = importlib.import_module(USED_SETTINGS)

settings_media_url = used_settings.MEDIA_URL
settings_media_root = used_settings.MEDIA_ROOT

settings_static_url = used_settings.STATIC_URL
settings_static_root = used_settings.STATIC_ROOT

### REGULAR IMPORTS ###
from django.conf.urls import url, include
from django.contrib import admin
from ticketsystem import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.redir_to_tickets),
    url(r'^', include('tickets.urls'))
] 

urlpatterns += static(settings_media_url, document_root=settings_media_root)

urlpatterns += static(settings_static_url, document_root=settings_static_root)

print(settings_static_url +"; "+settings_static_root)

