from django.core.exceptions import ValidationError
from django.test import TestCase
from app.models import DecisionTree, Node


class TestDecisionTreeModels(TestCase):

    @staticmethod
    def create_complex_decision_tree():
        tree = DecisionTree(slug='slug', title='title', description='description')
        tree.save()

        root_node = Node(criteria='mood')
        root_node.save()

        tree.root_node = root_node
        tree.save()

        happy = Node(predicate='happy', criteria='how happy')
        happy.save()

        very_happy = Node(predicate='very happy', criteria='i am glad to hear that')
        very_happy.save()

        kind_of_happy = Node(predicate='kind of happy', criteria='wish you were happier')
        kind_of_happy.save()

        happy.children.add(kind_of_happy)
        happy.children.add(very_happy)
        happy.save()

        root_node.children.add(happy)
        root_node.save()

        sad = Node(predicate='sad', criteria='i am sorry to hear that')
        sad.save()

        root_node.children.add(sad)
        root_node.save()

        melancholy = Node(predicate='just ok', criteria='ok then!')
        melancholy.save()

        root_node.children.add(melancholy)
        root_node.save()

    def test_retrieval_of_decision_tree(self):
        self.create_complex_decision_tree()
        tree = DecisionTree.objects.first()

        self.assertEqual(tree.slug, 'slug')
        self.assertEqual(tree.title, 'title')
        self.assertEqual(tree.description, 'description')

    def test_retrieval_of_decision_tree_nodes(self):
        self.create_complex_decision_tree()
        tree = DecisionTree.objects.first()

        self.assertEqual(tree.root_node.criteria, 'mood')
        self.assertEqual(tree.root_node.children.count(), 3)

        self.assertEqual(tree.root_node.children.all()[0].predicate, 'happy')
        self.assertEqual(tree.root_node.children.all()[0].criteria, 'how happy')

        happy_children = tree.root_node.children.all()[0].children.all()
        self.assertEqual(happy_children[0].predicate, 'very happy')
        self.assertEqual(happy_children[0].criteria, 'i am glad to hear that')
        self.assertEqual(happy_children[1].predicate, 'kind of happy')
        self.assertEqual(happy_children[1].criteria, 'wish you were happier')

        self.assertEqual(tree.root_node.children.all()[1].predicate, 'sad')
        self.assertEqual(tree.root_node.children.all()[1].criteria, 'i am sorry to hear that')

        self.assertEqual(tree.root_node.children.all()[2].predicate, 'just ok')
        self.assertEqual(tree.root_node.children.all()[2].criteria, 'ok then!')

    def test_duplicate_slugs_validation(self):
        DecisionTree(slug='yolo', title='swag').save()

        with self.assertRaises(ValidationError):
            DecisionTree(slug='yolo', title='swag-2').full_clean()
