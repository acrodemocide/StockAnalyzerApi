from api.models import Stock
from api.serializers import StockSerializer, PortfolioSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from services.service_registration import algorithm_registry
from api.serializers import PortfolioInputSerializer, PortfolioSerializer
from rest_framework.response import Response
from api.transfer_objs.portfolio_request import PortfolioRequest

from importlib.machinery import SourceFileLoader
PortfolioAnalyzerDriver = SourceFileLoader('PortfolioAnalyzerDriver', './PortfolioAnalyzerDriver.py').load_module()

# Create your views here.
class StockList(generics.ListCreateAPIView):

    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class StockDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class BackTestResults(APIView):
    def post(self, request, format=None):
        input_portfolio_serializer = PortfolioInputSerializer(data=request.data)
        input_portfolio_serializer.is_valid(raise_exception=True)
        serialized_input_portfolio = input_portfolio_serializer.save()
        user_portfolio = PortfolioRequest(
            serialized_input_portfolio.stocks,
            serialized_input_portfolio.strategy
            )
        
        value_snapshots = algorithm_registry[user_portfolio.strategy].backtest(user_portfolio.stocks)
        serializer = PortfolioSerializer(data=value_snapshots)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)