from rest_framework import viewsets
from .serializers import PortfolioInputSerializer, PortfolioSerializer
from rest_framework.response import Response
from .transferObjects.portfolio_request import PortfolioRequest
from .portfolio_analyzer import backtest

class PortfolioViewSet(viewsets.ViewSet):

    def create(self, request):
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