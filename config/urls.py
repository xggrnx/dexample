"""eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

from config.api import router
from user.views import CustomLoginView, set_language

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^set_language/$', set_language, name='set_language'),
    url(r'^', include('user.urls', namespace="user")),

    url(r'^login/$', CustomLoginView.as_view(), name='login'),
    url(r'^', include('market.urls', namespace="market")),
    url(r'^docs/', include_docs_urls(title='DJESHOP API', public=False, permission_classes=(AllowAny,))),
]
