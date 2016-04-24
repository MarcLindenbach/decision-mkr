from django.utils import text
from rest_framework import serializers
from app.models import Tree, Node
import itertools


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ListNodeSerializer(serializers.ModelSerializer):

    node_set = RecursiveField(many=True)

    class Meta:
        model = Node
        fields = ('predicate', 'criteria', 'node_set',)
        depth = 10


class NodeSerializer(serializers.ModelSerializer):

    parent = serializers.IntegerField(source='parent.pk', required=False)

    class Meta:
        model = Node
        fields = ('predicate', 'criteria', 'parent')
        depth = 10


class TreeSerializer(serializers.ModelSerializer):

    root_node = serializers.IntegerField(source='root_node.pk', required=False)

    class Meta:
        model = Tree
        fields = ('slug', 'title', 'description', 'root_node')
        read_only_fields = ('slug', )
        depth = 10

    def validate(self, data):
        if 'root_node' in data:
            root_pk = data['root_node']['pk']
            if not Node.objects.filter(id=root_pk).exists():
                raise serializers.ValidationError('Node %s does not exist' % root_pk)
        return data

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

    def update(self, instance, validated_data):
        if 'root_node' in validated_data:
            root_pk = validated_data.pop('root_node')['pk']
            instance.root_node = Node.objects.filter(id=root_pk).first()
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
