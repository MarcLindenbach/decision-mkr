from django.test import TestCase
from app.models import DecisionTree, DecisionNode
from app.serializers import DecisionTreeSerializer, DecisionTreeListSerializer, DecisionNodeSerializer


class DecisionTreeSerializerTest(TestCase):

    def create_decision_tree_using_serializer(self):
        serializer = DecisionTreeSerializer(data={'title': 'a tree',
                                                  'description': 'a description'})
        if not serializer.is_valid():
            self.fail(serializer.errors)
        serializer.save()

    def test_serializer_fails_with_no_title(self):
        serializer = DecisionTreeSerializer(data={'description': 'a description'})
        self.assertEqual(serializer.is_valid(), False)

    def test_serializer_creates_decision_tree_with_slug(self):
        self.create_decision_tree_using_serializer()

        self.assertEqual(DecisionTree.objects.count(), 1)
        decision_tree = DecisionTree.objects.first()
        self.assertEqual(decision_tree.slug, 'a-tree')
        self.assertEqual(decision_tree.title, 'a tree')
        self.assertEqual(decision_tree.description, 'a description')

    def test_serializer_creates_unique_slug_for_duplicate_titles(self):
        self.create_decision_tree_using_serializer()
        self.create_decision_tree_using_serializer()
        self.create_decision_tree_using_serializer()

        decision_trees = DecisionTree.objects.all()
        self.assertEqual(decision_trees[0].slug, 'a-tree')
        self.assertEqual(decision_trees[1].slug, 'a-tree-1')
        self.assertEqual(decision_trees[2].slug, 'a-tree-2')

    def test_serialize_decision_tree_displays_correct_data(self):
        DecisionTree(slug='a-tree', title='a tree', description='this is a tree').save()
        DecisionTree(slug='a-tree-1', title='a tree', description='this is a second tree').save()
        self.assertEqual(DecisionTree.objects.count(), 2)

        first_serializer = DecisionTreeSerializer(DecisionTree.objects.all()[0])
        second_serializer = DecisionTreeSerializer(DecisionTree.objects.all()[1])

        self.assertEqual(first_serializer.data['slug'], 'a-tree')
        self.assertEqual(first_serializer.data['title'], 'a tree')
        self.assertEqual(first_serializer.data['description'], 'this is a tree')
        self.assertIn('initial_node', first_serializer.data)

        self.assertEqual(second_serializer.data['slug'], 'a-tree-1')
        self.assertEqual(second_serializer.data['title'], 'a tree')
        self.assertEqual(second_serializer.data['description'], 'this is a second tree')
        self.assertIn('initial_node', second_serializer.data)


class DecisionTreeListSerializerTest(TestCase):

    def test_serialize_decision_tree_displays_correct_data(self):
        DecisionTree(slug='a-tree', title='a tree', description='this is a tree').save()
        DecisionTree(slug='a-tree-1', title='a tree', description='this is a second tree').save()
        self.assertEqual(DecisionTree.objects.count(), 2)

        first_serializer = DecisionTreeListSerializer(DecisionTree.objects.all()[0])
        second_serializer = DecisionTreeListSerializer(DecisionTree.objects.all()[1])

        self.assertEqual(first_serializer.data['slug'], 'a-tree')
        self.assertEqual(first_serializer.data['title'], 'a tree')
        self.assertEqual(first_serializer.data['description'], 'this is a tree')
        self.assertNotIn('initial_node', first_serializer.data)

        self.assertEqual(second_serializer.data['slug'], 'a-tree-1')
        self.assertEqual(second_serializer.data['title'], 'a tree')
        self.assertEqual(second_serializer.data['description'], 'this is a second tree')
        self.assertNotIn('initial_node', second_serializer.data)


class DecisionNodeSerializerTest(TestCase):
    def create_nested_decision_nodes(self):
        DecisionNode(text='yes-yes-node').save()                     # 0
        DecisionNode(text='yes-no-node').save()                      # 1
        DecisionNode(text='yes-node',                                # 2
                     yes_node=DecisionNode.objects.all()[0],
                     no_node=DecisionNode.objects.all()[1]).save()
        DecisionNode(text='no-node').save()                          # 3
        DecisionNode(text='first-node',                              # 4
                     yes_node=DecisionNode.objects.all()[2],
                     no_node=DecisionNode.objects.all()[3]).save()
        DecisionTree(slug='test', title='test', description='test', initial_node=DecisionNode.objects.last()).save()

    def test_serializer_fails_with_no_text(self):
        serializer = DecisionNodeSerializer(data={})
        self.assertEqual(serializer.is_valid(), False)

    def test_serialize_nested_decision_nodes(self):
        self.create_nested_decision_nodes()

        serializer = DecisionNodeSerializer(DecisionNode.objects.last())

        self.assertEqual(serializer.data['text'], 'first-node')
        self.assertEqual(serializer.data['yes_node']['text'], 'yes-node')
        self.assertEqual(serializer.data['yes_node']['yes_node']['text'], 'yes-yes-node')
        self.assertEqual(serializer.data['yes_node']['no_node']['text'], 'yes-no-node')
        self.assertEqual(serializer.data['no_node']['text'], 'no-node')

    def test_serializer_creates_decision_node(self):
        serializer = DecisionNodeSerializer(data={'text': 'a node'})

        if not serializer.is_valid():
            self.fail(serializer.errors)

        serializer.save()

        self.assertEqual(DecisionNode.objects.count(), 1)

        decision_node = DecisionNode.objects.first()
        self.assertEqual(decision_node.text, 'a node')

    def test_serializer_adds_decision_node_to_correct_tree(self):
        DecisionTree(slug='a-slug', title='a tree').save()
        decision_tree_slug = DecisionTree.objects.first().slug

        serializer = DecisionNodeSerializer(data={'decision_tree': decision_tree_slug,
                                                  'text': 'a node'})

        if not serializer.is_valid():
            self.fail(serializer.errors)

        serializer.save()

        decision_tree = DecisionTree.objects.first()
        self.assertEqual(decision_tree.initial_node.text, 'a node')

    def test_serializer_raises_error_if_tree_does_not_exist(self):
        serializer = DecisionNodeSerializer(data={'decision_tree': 'a-slug-that-does-not-exist',
                                                  'text': 'a node'})

        if serializer.is_valid():
            self.fail('Decision tree slug does not exist, this should have failed')

    def test_serializer_adds_yes_decision_node_to_correct_parent(self):
        DecisionNode(text='parent node').save()
        parent_node = DecisionNode.objects.first()

        serializer = DecisionNodeSerializer(data={'parent_yes_node': parent_node.pk,
                                                  'text': 'yes-node'})

        if not serializer.is_valid():
            self.fail(serializer.errors)

        serializer.save()

        parent_node = DecisionNode.objects.first()
        self.assertEqual(parent_node.yes_node.text, 'yes-node')

    def test_serializer_adds_no_decision_node_to_correct_parent(self):
        DecisionNode(text='parent node').save()
        parent_node = DecisionNode.objects.first()

        serializer = DecisionNodeSerializer(data={'parent_no_node': parent_node.pk,
                                                  'text': 'no-node'})

        if not serializer.is_valid():
            self.fail(serializer.errors)

        serializer.save()

        parent_node = DecisionNode.objects.first()
        self.assertEqual(parent_node.no_node.text, 'no-node')

    def test_serializer_raises_error_if_yes_parent_does_not_exist(self):
        serializer = DecisionNodeSerializer(data={'parent_yes_node': 1,
                                                  'text': 'a node'})

        if serializer.is_valid():
            self.fail('parent node does not exist, this should have failed')

    def test_serializer_raises_error_if_no_parent_does_not_exist(self):
        serializer = DecisionNodeSerializer(data={'parent_no_node': 1,
                                                  'text': 'a node'})

        if serializer.is_valid():
            self.fail('parent node does not exist, this should have failed')


