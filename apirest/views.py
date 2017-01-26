from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from apirest.serializers import UserSerializer, GroupSerializer, HouseSerializer, NodeSerializer, DataSerializer
from apirest.models import House, Node, ConsumptionData
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class HouseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = House.objects.all()
    serializer_class = HouseSerializer


class NodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class DataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ConsumptionData.objects.all()
    serializer_class = DataSerializer


def index(request):
    points = ConsumptionData.objects.all().order_by('-id')[:50][::-1]
    return render(request, 'index.html', {'node': 1,
                                          'points': points})