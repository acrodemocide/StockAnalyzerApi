from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from Analyzer.models import Stock
from Analyzer.serializers import StockSerializer


# Create your views here.
class StockList(APIView):
  """
    List all stocks, or create a new stock.
  """
  def get(self, request, format=None):
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)

  def post(elf, request, format=None):
    serializer = StockSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class StockDetail(APIView):
  """
    Retrieve, update or delete a stock.
  """

  def getStock(self, pk):
    try:
        return Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        raise Http404
  
  def get(self, request, pk, format=None):
    stock = self.getStock(pk)
    serializer = StockSerializer(stock)
    return Response(serializer.data)

  def put(self, request, pk, format=None):
    stock = self.getStock(pk)
    serializer = StockSerializer(stock, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    stock = self.getStock(pk)
    stock.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)