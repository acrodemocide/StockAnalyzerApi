from Analyzer.models import Stock, Portfolio
from Analyzer.serializers import StockSerializer, PortfolioSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from importlib.machinery import SourceFileLoader
PortfolioAnalyzerDriver = SourceFileLoader('PortfolioAnalyzerDriver', '../PortfolioAnalyzerDriver.py').load_module()

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
        stockSerializer = StockSerializer(data=request.data)

        portfolio = Portfolio()
        portfolio.price_history = PortfolioAnalyzerDriver.return_graph_vals()
        portfolioSerializer = PortfolioSerializer(portfolio)
        
        if stockSerializer.is_valid():
            return Response(portfolioSerializer.data)
        return Response(stockSerializer.errors, status=status.HTTP_400_BAD_REQUEST)