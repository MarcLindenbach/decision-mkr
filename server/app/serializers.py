from django.utils import text
from rest_framework import serializers
from app.models import DecisionTree, DecisionNode
import itertools


class DecisionNodeSerializer(serializers.ModelSerializer):
    decision_tree = serializers.IntegerField(required=False)

    class Meta:
        model = DecisionNode
        fields = ('decision_tree', 'text', 'yes_node', 'no_node')
        depth = 10

    def create(self, validated_data):
        return DecisionNode.objects.create(**validated_data)


class DecisionTreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DecisionTree
        fields = ('slug', 'title', 'description',)
        read_only_fields = ('slug', )
        depth = 10

    def create(self, validated_data):
        slug = text.slugify(validated_data['title'])

        if DecisionTree.objects.filter(slug=slug).exists():
            original_slug = slug
            for slug_prefix in itertools.count(1):
                slug = '%s-%d' % (original_slug, slug_prefix,)
                if not DecisionTree.objects.filter(slug=slug).exists():
                    break

        validated_data['slug'] = slug
        return DecisionTree.objects.create(**validated_data)

