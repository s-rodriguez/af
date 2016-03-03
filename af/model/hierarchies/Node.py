
class Node(object):

    def __init__(self, value, parent=None, nodes=None):
        self.value = value
        self.parent = parent
        self.nodes = nodes

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return self.nodes is None

    def add_node(self, node):
        if self.nodes is None:
            self.nodes = []
        self.nodes.append(node)
        node.parent = self

    def remove_node(self, node):
        self.nodes.remove(node)
        if len(self.nodes) == 0:
            self.nodes = None

    def __repr__(self):
        return str(self.value)
