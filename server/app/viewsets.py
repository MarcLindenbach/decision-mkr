from rest_framework import viewsets
from app.models import DecisionTree, DecisionNode
from app.serializers import DecisionTreeSerializer, DecisionTreeListSerializer, DecisionNodeSerializer


class DecisionTreeViewSet(viewsets.ModelViewSet):
    queryset = DecisionTree.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return DecisionTreeListSerializer
        else:
            return DecisionTreeSerializer


class DecisionNodeViewSet(viewsets.ModelViewSet):
    queryset = DecisionNode.objects.all()
    serializer_class = DecisionNodeSerializer
