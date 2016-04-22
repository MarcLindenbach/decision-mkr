from django.test import TestCase
from app.models import DecisionTree, DecisionNode
from app.serializers import DecisionTreeSerializer


class DecisionTreeSerializerTest(TestCase):

    def create_decision_tree_without_nodes(self):
        serializer = DecisionTreeSerializer(data={'title': 'a tree',
                                                  'description': 'a description'})
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

    def create_decision_tree_with_nodes(self):
        DecisionNode(text='Yes-Node').save()
        DecisionNode(text='No-Node').save()
        DecisionNode(text='First-Node',
                     yes_node=DecisionNode.objects.all()[0],
                     no_node=DecisionNode.objects.all()[1]).save()
        DecisionTree(slug='test', title='test', description='test', initial_node=DecisionNode.objects.last()).save()
        self.assertEqual(DecisionTree.objects.count(), 1)

    def test_serializer_creates_decision_tree_with_slug(self):
        self.create_decision_tree_without_nodes()

        self.assertEqual(DecisionTree.objects.count(), 1)
        decision_tree = DecisionTree.objects.first()
        self.assertEqual(decision_tree.slug, 'a-tree')
        self.assertEqual(decision_tree.title, 'a tree')
        self.assertEqual(decision_tree.description, 'a description')

    def test_serializer_creates_unique_slug_for_duplicate_titles(self):
        self.create_decision_tree_without_nodes()
        self.create_decision_tree_without_nodes()
        self.create_decision_tree_without_nodes()

        decision_trees = DecisionTree.objects.all()
        self.assertEqual(decision_trees[0].slug, 'a-tree')
        self.assertEqual(decision_trees[1].slug, 'a-tree-1')
        self.assertEqual(decision_trees[2].slug, 'a-tree-2')

    def test_serializer_serializes_decision_tree_without_nodes(self):
        DecisionTree(slug='a-tree', title='a tree', description='this is a tree').save()
        DecisionTree(slug='a-tree-1', title='a tree', description='this is a second tree').save()
        self.assertEqual(DecisionTree.objects.count(), 2)

        first_serializer = DecisionTreeSerializer(DecisionTree.objects.all()[0])
        second_serializer = DecisionTreeSerializer(DecisionTree.objects.all()[1])

        self.assertEqual(first_serializer.data['slug'], 'a-tree')
        self.assertEqual(first_serializer.data['title'], 'a tree')
        self.assertEqual(first_serializer.data['description'], 'this is a tree')

        self.assertEqual(second_serializer.data['slug'], 'a-tree-1')
        self.assertEqual(second_serializer.data['title'], 'a tree')
        self.assertEqual(second_serializer.data['description'], 'this is a second tree')

    def test_serializer_serializes_decision_tree_with_nodes(self):
        self.create_decision_tree_with_nodes()

        serializer = DecisionTreeSerializer(DecisionTree.objects.all()[0])

        self.assertEqual(serializer.data['slug'], 'test')
        self.assertEqual(serializer.data['initial_node']['text'], 'First-Node')
        self.assertEqual(serializer.data['initial_node']['yes_node']['text'], 'Yes-Node')
        self.assertEqual(serializer.data['initial_node']['no_node']['text'], 'No-Node')
