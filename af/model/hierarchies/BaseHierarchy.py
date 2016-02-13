

class BaseHierarchy(object):

    def __init__(self, name, root_node, leaf_nodes):
        self.name = name
        self.root_node = root_node
        self.leaf_nodes = leaf_nodes

    def get_leaf_node(self, leaf_node_value):
        for node in self.leaf_nodes:
            if node.value == leaf_node_value:
                return node
        return None

    def get_generalization_level_representation(self, starting_node, generalization_level):
        pass

    def add_node(self, parent_node, leaf_node):
        parent_node.add_node(leaf_node)


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

    def remove_node(self, node):
        self.nodes.remove(node)
        if len(self.nodes) == 0:
            self.nodes = None
