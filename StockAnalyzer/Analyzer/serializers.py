from rest_framework import serializers
from Analyzer.models import Stock

class StockSerializer(serializers.ModelSerializer):
  class Meta:
    model = Stock
    fields = ['businessName', 'ticker', 'price']