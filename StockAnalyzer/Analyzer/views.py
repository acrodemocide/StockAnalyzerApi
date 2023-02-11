from Analyzer.models import Stock, Portfolio
from Analyzer.serializers import StockSerializer, PortfolioSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
# from PortfolioAnalyzerDriver import return_graph_vals

from importlib.machinery import SourceFileLoader
PortfolioAnalyzerDriver = SourceFileLoader('PortfolioAnalyzerDriver', '../PortfolioAnalyzerDriver.py').load_module()
# PortfolioAnalyzerDriver.return_graph_vals()
# TestModule = SourceFileLoader('test', '../test.py').load_module()

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

        portfolioPriceHistory = PortfolioAnalyzerDriver.return_graph_vals()
        portfolio = Portfolio()
        portfolio.price_history = portfolioPriceHistory
        portfolioSerializer = PortfolioSerializer(portfolio)
        if stockSerializer.is_valid():
            # return Response(JSONRenderer().render(portfolioPriceHistory))
            return Response(portfolioSerializer.data)
        return Response(stockSerializer.errors, status=status.HTTP_400_BAD_REQUEST)