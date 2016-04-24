from django.utils import text
from rest_framework import serializers
from app.models import Tree, Node
import itertools


class TreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tree
        fields = ('slug', 'title', 'description', 'root_node')
        read_only_fields = ('slug', )
        depth = 10

    def create(self, validated_data):
        slug = text.slugify(validated_data['title'])

        if Tree.objects.filter(slug=slug).exists():
            original_slug = slug
            for slug_prefix in itertools.count(1):
                slug = '%s-%d' % (original_slug, slug_prefix,)
                if not Tree.objects.filter(slug=slug).exists():
                    break

        validated_data['slug'] = slug
        return Tree.objects.create(**validated_data)


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = ('predicate', 'criteria', 'children',)
        read_only_fields = ('children', )
        depth = 10
