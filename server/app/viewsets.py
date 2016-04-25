from rest_framework import viewsets
from app.models import Tree, Node
from app.serializers import TreeSerializer, NodeSerializer, NodeListSerializer


class TreeViewSet(viewsets.ModelViewSet):
    queryset = Tree.objects.all()
    lookup_field = 'slug'
    serializer_class = TreeSerializer


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NodeListSerializer
        else:
            return NodeSerializer
