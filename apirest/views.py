from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from apirest.serializers import UserSerializer, GroupSerializer, HouseSerializer, NodeSerializer, DataSerializer
from apirest.models import House, Node, ConsumptionData
from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
import json


@permission_classes((IsAuthenticated, ))
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

@permission_classes((IsAuthenticated, ))
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@permission_classes((IsAuthenticated, ))
class HouseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = House.objects.all()
    serializer_class = HouseSerializer

@permission_classes((IsAuthenticated, ))
class NodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

@permission_classes((IsAuthenticated, ))
class DataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ConsumptionData.objects.all()
    serializer_class = DataSerializer


@login_required(login_url="/admin/login/?next=/")
def index(request):
    houses = House.objects.filter(user=request.user)
    return render(request, 'index.html', {'houses': houses})


def last_reading(request):
    nodes = Node.objects.filter(house__user=request.user)
    total_usage = 0
    for node in nodes:
        total_usage += node.get_last_reading()
    data = [total_usage, [ node.getFormattedLastData() for node in nodes]]

    return HttpResponse(json.dumps(data))

@login_required
def toggle_node(request, node_id, state):
    node = get_object_or_404(Node, id=int(node_id))
    state = True if state == "true" else False
    node.relayState = state
    node.save()
    return HttpResponse("ok!")

