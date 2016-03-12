from af.exceptions import InfoException
from af.model.hierarchies.Node import Node


class BaseHierarchy(object):

    def __init__(self):
        self.leaf_nodes = []
        self.root_node = self.create_supression_node()

    def create_supression_node(self):
        value = '*'*10
        sup_node = Node(value, None, None)
        self.maintain_leaf_nodes(sup_node, action='add')
        return sup_node

    def get_leaf_node(self, leaf_node_value):
        for node in self.leaf_nodes:
            if node.value == leaf_node_value:
                return node
        return None

    def get_generalization_level_representation(self, starting_node, generalization_level):
        generalizated_node = starting_node
        for i in range(generalization_level):
            if generalizated_node.parent is None:
                break
            generalizated_node = generalizated_node.parent
        return generalizated_node

    def add_node(self, parent_node, leaf_node):
        parent_node.add_node(leaf_node)
        self.maintain_leaf_nodes(parent_node, action='remove')
        self.maintain_leaf_nodes(leaf_node, action='add')

    def find_node(self, node_value, starting_node=None):
        start = self.root_node if starting_node == None else starting_node
        if node_value == start.value:
            return start
        elif start.nodes is not None and len(start.nodes) > 0:
            for n in start.nodes:
                return self.find_node(node_value, n)
        else:
            return None

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

    def populate_nodes(self, parent_node, nodes, attribute_type):
        if isinstance(nodes, dict):
            for key, values in nodes.iteritems():
                node = Node(attribute_type(key))
                self.add_node(parent_node, node)
                self.populate_nodes(node, values, attribute_type)
        else:
            # leaf node, only the value
            self.add_node(parent_node, Node(attribute_type(nodes)))

        if self.validate_hierarchy_depth() is False:
            raise InfoException("Hierarchy depth is invalid")

    def transform(self, data_value, lvl):
        if lvl == 0:
            return data_value

        if self.root_node.nodes is None:
            return self.root_node.value

        data_node = self.get_leaf_node(data_value)
        if data_node is None:
            data_node = self.find_node(data_value)

        if data_node is not None:
            transformed_node = self.get_generalization_level_representation(data_node, lvl)
            return transformed_node.value

        raise InfoException("Couldnt find node with the value: %s" % data_value)

    #TODO: validate depth after populate
    def validate_hierarchy_depth(self):
        return True





