from app.models import Tree, Node


def create_complex_decision_tree():
    tree = Tree(slug='slug', title='title', description='description')
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