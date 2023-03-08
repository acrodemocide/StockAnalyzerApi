from django.contrib.auth.models import User, Group
from ..models import Portfolio
from rest_framework import serializers


class InputSerializer(serializers.Serializer):
    input = serializers.CharField()


################# TESTING CUSTOM SERIALIZER ######################
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
##################################################################

class PortfolioInputSerializer(serializers.Serializer):
    holdings = serializers.ListField(child=serializers.CharField(max_length=10))
    buy_and_hold_allocation = serializers.ListField(child=serializers.FloatField(min_value=0))
    tactical_rebalance_allocation = serializers.ListField(child=serializers.FloatField(min_value=0))