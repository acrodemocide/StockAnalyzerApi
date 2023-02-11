from rest_framework import serializers
from Analyzer.models import Stock, Portfolio

class StockSerializer(serializers.ModelSerializer):
  class Meta:
    model = Stock
    fields = ['id', 'businessName', 'ticker', 'price']

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['price_history']