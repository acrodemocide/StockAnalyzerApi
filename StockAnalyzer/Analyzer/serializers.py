from rest_framework import serializers
from Analyzer.models import Stock

class StockSerializer(serializers.ModelSerializer):
  class Meta:
    model = Stock
    fields = ['id', 'businessName', 'ticker', 'price']

class BackTestSerializer():
    def test():
        return 'hi'