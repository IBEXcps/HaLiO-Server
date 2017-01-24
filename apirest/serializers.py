from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apirest.models import House, Node, ConsumptionData


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class HouseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = House
        fields = ('url', 'nome', 'user')


class NodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'


class DataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConsumptionData
        fields = '__all__'

    def create(self, validated_data):
        return ConsumptionData.objects.create(**validated_data)