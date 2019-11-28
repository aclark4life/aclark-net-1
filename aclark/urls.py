"""aclarknet URL Configuration

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
from aclark.root import views as views_root
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from rest_framework import routers
from aclark.db import urls as urls_db
from aclark.db import views as views_db


from django.urls import path, re_path, include

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

router = routers.DefaultRouter()
router.register(r"clients", views_db.ClientViewSet)
router.register(r"testimonials", views_db.TestimonialViewSet)

urlpatterns = [
    url(r"^$", views_root.home, name="home"),
    url(r"^about$", views_root.about, name="about"),
    url(r"^admin", admin.site.urls),
    url(r"^api/", include(router.urls)),
    url(r"^db/", include(urls_db)),
    url(r"^blog$", views_root.blog, name="blog"),
    url(r"^clients$", views_root.clients, name="clients"),
    url(r"^contact$", views_root.contact, name="contact"),
    url(r"^about/team$", views_root.team, name="team"),
    url(r"^about/testimonials$", views_root.testimonials, name="testimonials"),
    url(r"^services$", views_root.services, name="services"),

    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^pages/', include(wagtail_urls)),
]

handler500 = "aclark.root.views.my_custom_error_view"
