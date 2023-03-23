from Analyzer.models import Stock
from Analyzer.serializers import StockSerializer, PortfolioSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from Analyzer.portfolio_analyzer import backtest
from Analyzer.serializers import PortfolioInputSerializer, PortfolioSerializer
from rest_framework.response import Response
from Analyzer.transferObjects.portfolio_request import PortfolioRequest

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
    def post(self, request, format=None):
        # stockSerializer = StockSerializer(data=request.data)

        # portfolio = Portfolio()
        # portfolio.price_history = PortfolioAnalyzerDriver.return_graph_vals()
        # portfolioSerializer = PortfolioSerializer(portfolio)
        
        # if stockSerializer.is_valid():
        #     return Response(portfolioSerializer.data)
        # return Response(stockSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        input_portfolio_serializer = PortfolioInputSerializer(data=request.data)
        input_portfolio_serializer.is_valid(raise_exception=True)
        serialized_input_portfolio = input_portfolio_serializer.save()
        user_portfolio = PortfolioRequest(
            serialized_input_portfolio.holdings,
            serialized_input_portfolio.buy_and_hold_allocation,
            serialized_input_portfolio.tactical_rebalance_allocation)

        portfolios = backtest(user_portfolio)
        serializer = PortfolioSerializer(instance=portfolios, many=True)
        return Response(serializer.data)