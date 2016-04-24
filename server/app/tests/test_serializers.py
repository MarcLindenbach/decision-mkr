from django.test import TestCase
from app.serializers import TreeSerializer, ListNodeSerializer, NodeSerializer
from app.models import Tree, Node
from .helpers import create_complex_decision_tree


class TreeSerializerTest(TestCase):

    def test_serialize_tree(self):
        create_complex_decision_tree()
        serializer = TreeSerializer(Tree.objects.first())

        self.assertEqual(serializer.data['slug'], 'slug')
        self.assertEqual(serializer.data['title'], 'title')
        self.assertEqual(serializer.data['description'], 'description')

    def test_create_tree(self):
        serializer = TreeSerializer(data={'title': 'a title', 'description': 'description'})

        if not serializer.is_valid():
            self.fail(serializer.errors)

        serializer.save()
        tree = Tree.objects.first()

        self.assertEqual(tree.slug, 'a-title')
        self.assertEqual(tree.title, 'a title')
        self.assertEqual(tree.description, 'description')

    def test_create_tree_with_duplicate_title_creates_unique_slug(self):
        Tree(slug='a-slug', title='a slug').save()
        serializer = TreeSerializer(data={'title': 'a slug'})

        if not serializer.is_valid():
            self.fail(serializer.errors)

        serializer.save()
        tree = Tree.objects.last()

        self.assertEqual(tree.slug, 'a-slug-1')

    def test_create_tree_with_no_data_is_invalid(self):
        serializer = TreeSerializer(data={})

        self.assertEqual(serializer.is_valid(), False)

    def test_update_tree(self):
        Tree(slug='a-slug', title='a slug').save()
        serializer = TreeSerializer(Tree.objects.first(), data={'title': 'new title', 'description': 'desc'})

        if not serializer.is_valid():
            self.fail(serializer.errors)

        serializer.save()
        tree = Tree.objects.first()

        self.assertEqual(tree.title, 'new title')
        self.assertEqual(tree.description, 'desc')

    def test_add_node_to_tree(self):
        Tree(slug='a-slug', title='a slug').save()
        Node(criteria='yolo').save()

        serializer = TreeSerializer(Tree.objects.first(), data={'root_node': Node.objects.first().id}, partial=True)

        if not serializer.is_valid():
            self.fail(serializer.errors)

        serializer.save()
        tree = Tree.objects.first()

        self.assertEqual(tree.root_node.criteria, 'yolo')

    def test_add_invalid_node_to_tree_is_invalid(self):
        serializer = TreeSerializer(data={'title': 'yolo', 'description': 'hello', 'root_node': 44})

        if serializer.is_valid():
            self.fail('Serializer is not valid, root_node of 44 should not exist')


class ListNodeSerializerTest(TestCase):

    def test_serialize_nodes(self):
        create_complex_decision_tree()
        serializer = ListNodeSerializer(Node.objects.first())

        self.assertEqual(serializer.data['criteria'], 'mood')

        mood_children = serializer.data['node_set']
        self.assertEqual(mood_children[0]['predicate'], 'happy')
        self.assertEqual(mood_children[1]['predicate'], 'sad')
        self.assertEqual(mood_children[2]['predicate'], 'just ok')

        self.assertEqual(mood_children[0]['criteria'], 'how happy')
        self.assertEqual(mood_children[1]['criteria'], 'i am sorry to hear that')
        self.assertEqual(mood_children[2]['criteria'], 'ok then!')

        happy_children = mood_children[0]['node_set']
        self.assertEqual(happy_children[0]['predicate'], 'very happy')
        self.assertEqual(happy_children[1]['predicate'], 'kind of happy')
        self.assertEqual(happy_children[0]['criteria'], 'i am glad to hear that')
        self.assertEqual(happy_children[1]['criteria'], 'wish you were happier')


class NodeSerializerTest(TestCase):

    def test_serialize_single_node(self):
        create_complex_decision_tree()
        serializer = NodeSerializer(Node.objects.first())

        self.assertEqual(serializer.data['criteria'], 'mood')
        self.assertEqual(serializer.data['parent'], None)

        serializer = NodeSerializer(Node.objects.all()[1])
        self.assertEqual(serializer.data['predicate'], 'happy')
        self.assertEqual(serializer.data['criteria'], 'how happy')
        self.assertEqual(serializer.data['parent'], 1)
