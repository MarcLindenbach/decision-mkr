from rest_framework import viewsets
from app.models import DecisionTree, DecisionNode
from app.serializers import DecisionTreeSerializer, DecisionNodeSerializer


class DecisionTreeViewSet(viewsets.ModelViewSet):
    queryset = DecisionTree.objects.all()
    serializer_class = DecisionTreeSerializer
    lookup_field = 'slug'


class DecisionNodeViewSet(viewsets.ModelViewSet):
    queryset = DecisionNode.objects.all()
    serializer_class = DecisionNodeSerializer
