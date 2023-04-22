# url for quickstart app
"""Defines URL patterns for quickstart"""
from django.conf.urls import url
from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'folios', views.PortfolioViewSet, basename='folios')
urlpatterns = [
    # Home page
    url(r'', include(router.urls)),
    #path('test_ViewSet', views.Folios, name='test_ViewSet'),
    #path('test_view', views.PortfolioView, name='test_view'),
    #path('', include(router.urls)),
    #url(r'^$', views.PortfolioViewSet.as_view())#, name='folios') #why is it named 'index'?...
]