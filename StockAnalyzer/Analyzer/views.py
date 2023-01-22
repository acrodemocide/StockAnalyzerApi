from Analyzer.models import Stock
from Analyzer.serializers import StockSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class StockList(generics.ListCreateAPIView):

    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class StockDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class BackTestResults(APIView):
    
    # Create portfolio -- this will return the backtest results
    def post(self, request, format=None):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)