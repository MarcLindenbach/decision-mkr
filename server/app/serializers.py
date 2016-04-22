from django.utils import text
from rest_framework import serializers
from app.models import DecisionTree
import itertools


class DecisionTreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DecisionTree
        fields = ('slug', 'title', 'description', 'initial_node',)
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
        return super().create(validated_data)

