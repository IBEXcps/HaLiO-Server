from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from apirest.serializers import UserSerializer, GroupSerializer, HouseSerializer, NodeSerializer, DataSerializer
from apirest.models import House, Node, ConsumptionData
from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required


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


@login_required(login_url="api-auth/login/?next=/")
def index(request):
    points = ConsumptionData.objects.all().order_by('-timestamp')[:500][::-1]
    houses = House.objects.filter(user=request.user)
    nodes = Node.objects.filter(house__user=request.user)

    return render(request, 'index.html', {'node': 1,
                                          'points': points,
                                          'houses': houses,
                                          'nodes': nodes})


def last_reading(request, node_id):
    node = get_object_or_404(Node,id=node_id)
    last_value = node.get_last_reading()
    return HttpResponse(str(last_value))


def toggle_node(request, node_id, state):
    node = get_object_or_404(Node, id=int(node_id))
    state = True if state == "true" else False
    node.relayState = state
    node.save()
    return HttpResponse("ok!")

