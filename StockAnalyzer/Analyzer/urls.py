from django.urls import path
from Analyzer import views

urlpatterns = [
    path('stocks/', views.StockList),
    path('stocks/<int:pk>/', views.StockDetail)
]
