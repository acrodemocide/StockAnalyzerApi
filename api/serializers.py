from rest_framework import serializers
from api.models import Stock, Portfolio
from api.transfer_objs.portfolio_response import Portfolio
from api.transfer_objs.portfolio_request import PortfolioRequest
from rest_framework import serializers

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

class OutputPortfolioSerializer(serializers.Serializer):
    snapshots = serializers.DictField(
        child=serializers.FloatField(min_value=0),
        help_text="A dictionary mapping datetime to portfolio values."
    )
    benchmark = serializers.DictField(
        child=serializers.FloatField(min_value=0),
        help_text="A dictionary mapping datetime to benchmark values."
    )

    def to_representation(self, instance):
        def convert_keys_to_strings(data):
            return {key.isoformat(): value for key, value in data.items()}
        
        return {
            'snapshots': convert_keys_to_strings(instance.snapshots),
            'benchmark': convert_keys_to_strings(instance.benchmark),
        }

class PortfolioInputSerializer(serializers.Serializer):
    stocks = serializers.DictField(child=serializers.FloatField(min_value=0))
    strategy = serializers.CharField(max_length=256)
    initial_value = serializers.FloatField(min_value=0)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    benchmark_ticker = serializers.CharField(max_length=256, allow_blank=True)

    def create(self, validated_data):
        return PortfolioRequest(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance