from Analyzer.models import Stock
from Analyzer.serializers import StockSerializer
from rest_framework import generics

# Create your views here.
class StockList(generics.ListCreateAPIView):

  queryset = Stock.objects.all()
  serializer_class = StockSerializer

class StockDetail(generics.RetrieveUpdateDestroyAPIView):

  queryset = Stock.objects.all()
  serializer_class = StockSerializer
    