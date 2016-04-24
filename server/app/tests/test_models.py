from django.core.exceptions import ValidationError
from django.test import TestCase
from app.models import Tree, Node
from .helpers import create_complex_decision_tree


class TestDecisionTreeModels(TestCase):

    def test_retrieval_of_tree(self):
        create_complex_decision_tree()
        tree = Tree.objects.first()

        self.assertEqual(tree.slug, 'slug')
        self.assertEqual(tree.title, 'title')
        self.assertEqual(tree.description, 'description')

    def test_retrieval_of_tree_nodes(self):
        create_complex_decision_tree()
        tree = Tree.objects.first()
        root_node = tree.root_node

        self.assertEqual(root_node.criteria, 'mood')
        self.assertEqual(root_node.node_set.count(), 3)

        self.assertEqual(root_node.node_set.all()[0].predicate, 'happy')
        self.assertEqual(root_node.node_set.all()[0].criteria, 'how happy')

        happy_node_set = root_node.node_set.all()[0].node_set.all()
        self.assertEqual(happy_node_set[0].predicate, 'very happy')
        self.assertEqual(happy_node_set[0].criteria, 'i am glad to hear that')
        self.assertEqual(happy_node_set[1].predicate, 'kind of happy')
        self.assertEqual(happy_node_set[1].criteria, 'wish you were happier')

        self.assertEqual(root_node.node_set.all()[1].predicate, 'sad')
        self.assertEqual(root_node.node_set.all()[1].criteria, 'i am sorry to hear that')

        self.assertEqual(root_node.node_set.all()[2].predicate, 'just ok')
        self.assertEqual(root_node.node_set.all()[2].criteria, 'ok then!')

    def test_duplicate_slug_validation(self):
        Tree(slug='yolo', title='swag').save()

        with self.assertRaises(ValidationError):
            Tree(slug='yolo', title='swag-2').full_clean()
