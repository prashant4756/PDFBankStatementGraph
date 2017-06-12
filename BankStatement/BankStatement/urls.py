"""BankStatement URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from BankStatementApp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^BankStatementApp/mylink/$', views.my_link_view, name='mylink'),
    url(r'^BankStatementApp/$', views.model_form_upload, name='model_form_upload'),
    url(r'^BankStatementApp/dashboard/$', views.for_dashboard, name='for_dashboard')
]

if settings.DEBUG:
	urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)