from rest_framework import viewsets
from app.models import Tree


class TreeViewSet(viewsets.ModelViewSet):
    queryset = Tree.objects.all()

