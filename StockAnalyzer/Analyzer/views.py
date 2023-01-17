# from rest_framework import status
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
from Analyzer.models import Stock
from Analyzer.serializers import StockSerializer
from rest_framework import mixins
from rest_framework import generics

# Create your views here.
class StockList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):

  queryset = Stock.objects.all()
  serializer_class = StockSerializer
  
  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)
        

class StockDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):

  queryset = Stock.objects.all()
  serializer_class = StockSerializer

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)

  def put(self, request, *args, **kwargs):
    return self.update(request, *args, **kwargs)
    
  def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)
    