from Analyzer.models import Stock
from Analyzer.serializers import StockSerializer
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
        resultTuple = PortfolioAnalyzerDriver.return_graph_vals()
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            # return Response(serializer.data)
            return Response(JSONRenderer().render(resultTuple))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)