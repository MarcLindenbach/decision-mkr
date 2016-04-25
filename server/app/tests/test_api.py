from app.models import Tree, Node
from rest_framework.test import APITestCase
from .helpers import create_complex_decision_tree


class ApiTest(APITestCase):

    def create_trees(self):
        Tree(slug='slug-1', title='first title', description='1st description').save()
        Tree(slug='slug-2', title='second title', description='2nd description').save()
        Tree(slug='slug-3', title='third title', description='3rd description').save()
        self.assertEqual(Tree.objects.count(), 3)

    def test_get_tree(self):
        self.create_trees()
        response = self.client.get('/trees/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['slug'], 'slug-1')
        self.assertEqual(response.data[0]['title'], 'first title')
        self.assertEqual(response.data[0]['description'], '1st description')
        self.assertEqual(response.data[1]['slug'], 'slug-2')
        self.assertEqual(response.data[1]['title'], 'second title')
        self.assertEqual(response.data[1]['description'], '2nd description')
        self.assertEqual(response.data[2]['slug'], 'slug-3')
        self.assertEqual(response.data[2]['title'], 'third title')
        self.assertEqual(response.data[2]['description'], '3rd description')

    def test_retrieve_tree(self):
        self.create_trees()
        response = self.client.get('/trees/slug-1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['slug'], 'slug-1')
        self.assertEqual(response.data['title'], 'first title')
        self.assertEqual(response.data['description'], '1st description')

    def test_post_tree(self):
        self.create_trees()
        response = self.client.post('/trees/', {'title': 'new title', 'description': 'yolo'})

        self.assertEqual(response.status_code, 201)
        tree = Tree.objects.last()
        self.assertEqual(tree.slug, 'new-title')
        self.assertEqual(tree.title, 'new title')
        self.assertEqual(tree.description, 'yolo')

    def test_post_tree_duplicate_title(self):
        self.create_trees()
        response = self.client.post('/trees/', {'title': 'slug 1', 'description': 'yolo'})

        self.assertEqual(response.status_code, 201)
        tree = Tree.objects.last()
        self.assertEqual(tree.slug, 'slug-1-1')
        self.assertEqual(tree.title, 'slug 1')
        self.assertEqual(tree.description, 'yolo')

    def test_post_tree_no_title(self):
        response = self.client.post('/trees/', {'description': 'yolo'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'title': ['This field is required.']})

    def test_post_tree_with_root_node(self):
        Node(criteria='criteria').save()
        response = self.client.post('/trees/', {'title': 'slug 1', 'description': 'yolo', 'root_node': 1})

        self.assertEqual(response.status_code, 201)
        tree = Tree.objects.last()
        self.assertEqual(tree.root_node.criteria, 'criteria')

    def test_post_tree_with_invalid_root_node(self):
        create_complex_decision_tree()
        response = self.client.post('/trees/', {'title': 'slug 1', 'description': 'yolo', 'root_node': 1})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'non_field_errors': ['Node 1 attached to another list']})

        response = self.client.post('/trees/', {'title': 'slug 1', 'description': 'yolo', 'root_node': 999})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'non_field_errors': ['Node 999 does not exist']})

    def test_put_tree(self):
        pass

    def test_patch_tree(self):
        pass

