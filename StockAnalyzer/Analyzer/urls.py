from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Analyzer import views

urlpatterns = [
    path('stocks/', views.StockList.as_view()),
    path('stocks/<int:pk>/', views.StockDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)