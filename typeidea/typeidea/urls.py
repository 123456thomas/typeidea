"""typeidea URL Configuration

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

from blog.views import (SearchView, PostDetailView, IndexView, CategoryView, TagView, AuthorView)
from config.views import links
from .custom_site import custom_site

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category_list'),
    url(r'^tag/(<?P<tag_id>\d+)/$', TagView.as_view(), name='tag_list'),
    url(r'^post/(?P<post_id>\d+)\.html$', PostDetailView.as_view(), name='post_detail'),
    url(r'^links/$', links, name='links'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^user/(?P<user_id>\d+)$', AuthorView.as_view(), name='user'),
    url(r'^super_admin/', admin.site.urls, name='super_admin'),
    url(r'^admin/', custom_site.urls, name='admin'),
]
