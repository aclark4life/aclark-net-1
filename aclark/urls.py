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
from aclark.db import urls as urls_db
from aclark.db import views as views_db
from aclark.root import views as views_root
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'clients', views_db.ClientViewSet)
router.register(r'services', views_db.ServiceViewSet)
router.register(r'testimonials', views_db.TestimonialViewSet)
router.register(r'profiles', views_db.ProfileViewSet)

urlpatterns = [
    url(r'^$', views_root.home, name='home'),
    url(r'^about$', views_root.about, name='about'),
    url(r'^admin', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^db/', include(urls_db)),
    url(r'^blog$', views_root.blog, name='blog'),
    url(r'^clients$', views_root.clients, name='clients'),
    url(r'^contact$', views_root.contact, name='contact'),
    url(r'^services$', views_root.services, name='services'),
    url(r'^team$', views_root.team, name='team'),
    url(r'^testimonials$', views_root.testimonials, name='testimonials'),
]
