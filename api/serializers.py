from rest_framework import serializers
from api.models import Stock, Portfolio
from .transferObjects.PortfolioResponse import Portfolio
from .transferObjects.portfolio_request import PortfolioRequest

class StockSerializer(serializers.ModelSerializer):
  class Meta:
    model = Stock
    fields = ['id', 'businessName', 'ticker', 'price']

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['price_history']

class InputSerializer(serializers.Serializer):
    input = serializers.CharField()

class PortfolioSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    buy_and_hold_final_value = serializers.FloatField(max_value=None, min_value=0)
    tactical_rebalance_final_value = serializers.FloatField(max_value=None, min_value=0)
    buy_and_hold_allocation = serializers.ListField(child=serializers.FloatField(min_value=0))
    tactical_rebalance_allocation = serializers.ListField(child=serializers.FloatField(min_value=0))
    buy_and_hold_graph_data = serializers.ListField(child=serializers.FloatField(min_value=0))
    tactical_rebalance_graph_data = serializers.ListField(child=serializers.FloatField(min_value=0))
    holdings = serializers.ListField(child=serializers.CharField(max_length=10))

    def create(self, validated_data):
        return Portfolio(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance

class PortfolioInputSerializer(serializers.Serializer):
    holdings = serializers.ListField(child=serializers.CharField(max_length=10))
    buy_and_hold_allocation = serializers.ListField(child=serializers.FloatField(min_value=0))
    tactical_rebalance_allocation = serializers.ListField(child=serializers.FloatField(min_value=0))

    def create(self, validated_data):
        return PortfolioRequest(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
