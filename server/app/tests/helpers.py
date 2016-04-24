from app.models import Tree, Node


def create_complex_decision_tree():
    tree = Tree(slug='slug', title='title', description='description')
    tree.save()

    root_node = Node(criteria='mood')
    root_node.save()

    tree.root_node = root_node
    tree.save()

    happy = Node(predicate='happy', criteria='how happy', parent=root_node)
    happy.save()

    very_happy = Node(predicate='very happy', criteria='i am glad to hear that', parent=happy)
    very_happy.save()

    kind_of_happy = Node(predicate='kind of happy', criteria='wish you were happier', parent=happy)
    kind_of_happy.save()

    sad = Node(predicate='sad', criteria='i am sorry to hear that', parent=root_node)
    sad.save()

    melancholy = Node(predicate='just ok', criteria='ok then!', parent=root_node)
    melancholy.save()
