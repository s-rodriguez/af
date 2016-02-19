

class BaseHierarchy(object):

    def __init__(self, root_node, leaf_nodes):
        self.root_node = root_node
        self.leaf_nodes = leaf_nodes

    def get_leaf_node(self, leaf_node_value):
        for node in self.leaf_nodes:
            if node.value == leaf_node_value:
                return node
        return None

    def get_generalization_level_representation(self, starting_node, generalization_level, supress_if_none=True):
        generalizated_node = starting_node
        for i in range(generalization_level):
            if generalizated_node.parent is not None:
                generalizated_node = generalizated_node.parent
            elif supress_if_none:
                generalizated_node = BaseHierarchy.supression_node(generalizated_node)
        return generalizated_node

    def add_node(self, parent_node, leaf_node):
        parent_node.add_node(leaf_node)
        self.maintain_leaf_nodes(parent_node, action='remove')
        self.maintain_leaf_nodes(leaf_node, action='add')

    def maintain_leaf_nodes(self, node, action='add'):
        if action == 'add':
            self.leaf_nodes.append(node)
        elif action == 'remove':
            if node in self.leaf_nodes:
                self.leaf_nodes.remove(node)
        else:
            raise Exception('Unknown action requested')

    def print_hierarchy(self, parent_node=None, level=0):
        parent_node = self.root_node if parent_node is None else parent_node
        print '\t'*level + str(parent_node.value)
        next_level = level + 1
        if parent_node.nodes is not None:
            for node in parent_node.nodes:
                self.print_hierarchy(node, next_level)

    def hierarchy_representation(self, nodes=None):
        walk_nodes = [self.root_node] if nodes is None else nodes
        hierarchy = {}
        for node in walk_nodes:
            if node.nodes is not None:
                hierarchy[node.value] = self.hierarchy_representation(node.nodes)
            else:
                return node.value
        return hierarchy

    def populate_nodes(self, parent_node, nodes):
        import pdb; pdb.set_trace()
        if isinstance(nodes, dict):
            for key, values in nodes.iteritems():
                node = Node(key)
                self.add_node(parent_node, node)
                self.populate_nodes(node, values)
        else:
            # leaf node, only the value
            import pdb; pdb.set_trace()
            self.add_node(parent_node, Node(nodes))

    @staticmethod
    def supression_node(node):
        value = '*'*10
        sup_node = Node(value, None, node)
        return sup_node

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
