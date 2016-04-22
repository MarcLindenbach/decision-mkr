from django.utils import text
from rest_framework import serializers
from app.models import DecisionTree, DecisionNode
import itertools


class DecisionNodeSerializer(serializers.ModelSerializer):
    decision_tree = serializers.CharField(max_length=50, required=False)
    parent_yes_node = serializers.IntegerField(required=False)
    parent_no_node = serializers.IntegerField(required=False)

    class Meta:
        model = DecisionNode
        fields = ('parent_yes_node', 'parent_no_node', 'decision_tree', 'text', 'yes_node', 'no_node')
        read_only_fields =('yes_node', 'no_node')
        depth = 10

    def validate(self, data):
        if 'decision_tree' in data:
            slug = data['decision_tree']
            if not DecisionTree.objects.filter(slug=slug).exists():
                raise serializers.ValidationError('No decision tree exists with slug %s' % slug)

        if 'parent_yes_node' in data:
            pk = int(data['parent_yes_node'])
            if not DecisionNode.objects.filter(pk=pk).exists():
                raise serializers.ValidationError('No parent node exists with pk %d' % pk)

        if 'parent_no_node' in data:
            pk = int(data['parent_no_node'])
            if not DecisionNode.objects.filter(pk=pk).exists():
                raise serializers.ValidationError('No parent node exists with pk %d' % pk)
            
        return data

    def create(self, validated_data):
        slug = ''
        if 'decision_tree' in validated_data:
            slug = validated_data.pop('decision_tree')

        decision_node = DecisionNode.objects.create(**validated_data)

        if slug:
            decision_tree = DecisionTree.objects.filter(slug=slug).first()
            decision_tree.initial_node = decision_node
            decision_tree.save()

        return decision_node


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

