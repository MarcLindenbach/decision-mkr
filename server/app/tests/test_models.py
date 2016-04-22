from django.core.exceptions import ValidationError
from django.test import TestCase
from app.models import DecisionTree, DecisionNode


class DecisionTreeAndNodeModelTest(TestCase):

    def test_creation_and_retrieval_of_decision_trees(self):
        DecisionTree(slug='A-new-node', title='A new node', description='Hello world!').save()
        DecisionTree(slug='A-second-node', title='A new node', description='Hello world!').save()

        self.assertEqual(DecisionTree.objects.first().slug, 'A-new-node')
        self.assertEqual(DecisionTree.objects.last().slug, 'A-second-node')

    def test_duplicate_slug_raises_exception(self):
        DecisionTree(slug='A-new-node', title='A new node', description='Hello world!').save()

        with self.assertRaises(ValidationError):
            DecisionTree(slug='A-new-node', title='A new node', description='Hello world!').full_clean()

    def test_creation_and_retrieval_of_decision_node(self):
        DecisionNode(text='Hello world!').save()
        DecisionNode(text='Goodbye world!').save()

        self.assertEqual(DecisionNode.objects.first().text, 'Hello world!')
        self.assertEqual(DecisionNode.objects.last().text, 'Goodbye world!')

    def test_creation_and_retrieval_of_linked_decision_nodes(self):
        DecisionNode(text='Yes-Node').save()
        DecisionNode(text='No-Node').save()
        DecisionNode(text='First-Node',
                     yes_node=DecisionNode.objects.all()[0],
                     no_node=DecisionNode.objects.all()[1]).save()

        initial_node = DecisionNode.objects.last()
        self.assertEqual(DecisionNode.objects.count(), 3)
        self.assertEqual(initial_node.text, 'First-Node')
        self.assertEqual(initial_node.yes_node.text, 'Yes-Node')
        self.assertEqual(initial_node.no_node.text, 'No-Node')

    def test_creation_and_retrieval_of_decision_tree_with_one_node(self):
        DecisionNode(text='Yolo').save()
        DecisionTree(slug='test', title='test', description='test', initial_node=DecisionNode.objects.first()).save()
        decision_tree = DecisionTree.objects.first()

        self.assertEqual(decision_tree.initial_node.text, 'Yolo')

    def test_creation_and_retrieval_of_decision_tree_with_linked_nodes(self):
        DecisionNode(text='Yes-Node').save()
        DecisionNode(text='No-Node').save()
        DecisionNode(text='First-Node',
                     yes_node=DecisionNode.objects.all()[0],
                     no_node=DecisionNode.objects.all()[1]).save()
        DecisionTree(slug='test', title='test', description='test', initial_node=DecisionNode.objects.last()).save()

        decision_tree = DecisionTree.objects.first()
        self.assertEqual(decision_tree.initial_node.text, 'First-Node')
        self.assertEqual(decision_tree.initial_node.yes_node.text, 'Yes-Node')
        self.assertEqual(decision_tree.initial_node.no_node.text, 'No-Node')
