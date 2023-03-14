# url for quickstart app
"""Defines URL patterns for quickstart"""
from django.conf.urls import url
from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'folios', views.PortfolioViewSet, basename='folios')
urlpatterns = [
    url(r'', include(router.urls)),
]