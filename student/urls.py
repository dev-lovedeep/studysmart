"""student URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from website.views import homeview, download_view, productview, simple_upload, subject_view, contact_view, setcontent_view
from django.conf import settings
from django.conf.urls.static import static


import django.views.defaults


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', homeview, name="home"),
    path('set', setcontent_view, name="content"),
    path('buy', productview, name="buysell"),
    path('upload', simple_upload, name="upload"),
    path('books', subject_view, name="books"),
    path('paper', subject_view, name="paper"),
    path('contact', contact_view, name="contact"),
    path('books/<str:name>/', download_view, name="books"),
    path('paper/<str:name>/', download_view, name="books"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
