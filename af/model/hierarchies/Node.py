
class Node(object):
    """Class node use in the hierarchies.

    """
    def __init__(self, value, parent=None, nodes=None):
        self.value = value
        self.parent = parent
        self.nodes = nodes

    def is_root(self):
        """Checks if it is a root node or not, based on its parent

        :rtype: Boolean indicating if it is a root node or not.

        """
        return self.parent is None

    def is_leaf(self):
        """Checks if it is a leaf node or not, based on its leaf nodes

        :rtype: Boolean indicating if it is a leaf node or not.

        """
        return self.nodes is None

    def add_node(self, node):
        """Add a new node as a son

        :param node: New node to be added into the nodes son list.

        """
        if self.nodes is None:
            self.nodes = []
        self.nodes.append(node)
        node.parent = self

    def remove_node(self, node):
        """Remove a node from the sons list

        :param node: Node to be removed

        """
        self.nodes.remove(node)
        if len(self.nodes) == 0:
            self.nodes = None

    def get_leaf_node(self, value):
        """Given a value, look for the node associated with it
        among the leaf nodes.

        :param value: value of the node being looked for
        :rtype: Node with value looked

        """
        if self.nodes is not None:
            for node in self.nodes:
                if node.value == value:
                    return node
        return None

    def __repr__(self):
        return str(self.value)
