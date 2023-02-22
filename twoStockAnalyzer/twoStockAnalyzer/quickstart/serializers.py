from django.contrib.auth.models import User, Group
from .models import Portfolio
from rest_framework import serializers
from . import views


class InputSerializer(serializers.Serializer):
    input = serializers.CharField()


################# TESTING CUSTOM SERIALIZER ######################
class PortfolioSerializer(serializers.Serializer):
    #class Meta:
    #    model = Portfolio
    #    fields = ['url', 'name', 'value']

    id = serializers.IntegerField(min_value=0)
    name = serializers.CharField(max_length=256)
    b_and_h_value = serializers.FloatField(max_value=None, min_value=0)
    tactical_rebal_value = serializers.FloatField(max_value=None, min_value=0)
    b_and_h_allocation = serializers.ListField(child=serializers.FloatField(min_value=0))
    tactical_rebal_allocation = serializers.ListField(child=serializers.FloatField(min_value=0))
    bh_graph_data = serializers.ListField(child=serializers.FloatField(min_value=0))
    tr_graph_data = serializers.ListField(child=serializers.FloatField(min_value=0))
    holdings = serializers.ListField(child=serializers.CharField(max_length=10))

    def create(self, validated_data):
        return Portfolio(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
##################################################################
        
    

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
