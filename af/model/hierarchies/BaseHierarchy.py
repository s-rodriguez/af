from af.exceptions import InfoException
from af.model.hierarchies.Node import Node


class BaseHierarchy(object):
    """Class that used as a model of Hierarchy.
    A hierarchy can be of a supression or generalization kind. The only difference between both kinds, is that the supression hierarchy transforms every value into the same supression value, and the generalization hierarchy transforms a value into the value that is one level up.

    """
    def __init__(self):
        self.leaf_nodes = []
        self.root_node = self.create_supression_node()

    def create_supression_node(self):
        """Creates the basic supression node to be used on every hierarchy.
        A supression node is a GLGNode that has '**********' as a value, and no parent

        :rtype: Supression Node

        """
        sup_node = self.supression_node()
        self.maintain_leaf_nodes(sup_node, action='add')
        return sup_node

    @staticmethod
    def supression_node():
        """Returns a supression node

        :rtype: Node

        """
        value = '*'*10
        sup_node = Node(value, None, None)
        return sup_node

    def get_leaf_node(self, leaf_node_value):
        """Given a value that supposedly belongs to a leaf node, find the node and return it.

        :param string leaf_node_value: Value of the node
        :rtype: Node containing the leaf_node_value

        """
        for node in self.leaf_nodes:
            if node.value == leaf_node_value:
                return node
        return None

    def get_generalization_level_representation(self, starting_node, generalization_level):
        """Given a node, transform it to a certain generalization level

        :param starting_node: Instance of a Node.
        :param int generalization_level: Value of the level it is intended for the node to be generalized.
        :rtype: The starting node generalization.

        """
        generalizated_node = starting_node
        for i in range(generalization_level):
            if generalizated_node.parent is None:
                break
            generalizated_node = generalizated_node.parent
        return generalizated_node

    def add_node(self, parent_node, leaf_node):
        """Add a new node to the current hierarchy

        :param parent_node: Node that acts as a parent of the node that is to be added to the hierarchy
        :param leaf_node: New node to add

        """
        parent_node.add_node(leaf_node)
        self.maintain_leaf_nodes(parent_node, action='remove')
        self.maintain_leaf_nodes(leaf_node, action='add')

    def find_node(self, node_value, starting_node=None):
        """Given a node value, find it's corresponding Node

        :param string node_value: Value of the node
        :param starting_node: Node (None by default). Used for recursion and knowing where is the finding cursor located
        :rtype: Node with the node_value

        """
        start = self.root_node if starting_node == None else starting_node
        if node_value == start.value:
            return start
        elif start.nodes is not None and len(start.nodes) > 0:
            for n in start.nodes:
                temp = self.find_node(node_value, n)
                if temp is not None:
                    return temp
        else:
            return None

    def maintain_leaf_nodes(self, node, action='add'):
        """Every time we add or remove a leaf node, the leaf node cache list has to be maintained.

        :param node: Node we want to add/remove
        :param string action: Action we want to perform (add, remove)

        """
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

    def hierarchy_representation(self, node=None):
        """Returns the hierarchy representation in the form of a dictionary

        :param node: Node (Default None) Used for recursion levels.
        :rtype: Dictionary representation of the hierarchy

        """
        walk_node = self.root_node if node is None else node
        hierarchy = {}
        if walk_node.nodes is not None:
            hierarchy[walk_node.value] = {}
            for node in walk_node.nodes:
                hierarchy[walk_node.value].update(self.hierarchy_representation(node))
        else:
            hierarchy[walk_node.value] = None
            return hierarchy
        return hierarchy

    def populate_nodes(self, parent_node, nodes, attribute_type):
        """This method is to be used every time a hierarchy is loaded, and the nodes are populated inside of it.

        :param parent_node: Node indicating the current parent to which all the nodes are to be put below
        :param dict nodes: Dictionary containing all the information about the nodes, its values and son nodes.
        :param attribute_type: The type of the node value.

        """
        if isinstance(nodes, dict):
            for key, values in nodes.iteritems():
                node = Node(attribute_type(key))
                self.add_node(parent_node, node)
                self.populate_nodes(node, values, attribute_type)

    def transform(self, data_value, lvl):
        """Given a certain data value, and a level, look for it the node containing that value, and get the generalization level representation of the lvl

        :param string data_value: Value of the Node
        :param int lvl: Level inteded to generalize the node
        :rtype: Value of the node that has been transformed to the generalization level.

        """
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

    def transform_leaf_nodes(self, lvl=1):
        """Transform all leaf nodes to a certain level.

        :param int lvl: Generalization level to which we want to take all leaf nodes.
        :rtype: List containing the values of all the transformed leaf nodes.

        """
        anonymized_data = {}
        for leaf in self.leaf_nodes:
            transformed_node = self.get_generalization_level_representation(leaf, lvl)
            anonymized_data[leaf.value] = transformed_node.value
        return anonymized_data

    def validate_hierarchy_depth(self):
        """After a hierarchy has been populated, and before using it, it must be validated that it has a symmetrical depth

        :rtype: Boolean indicating if the hierarchy is valid or not.

        """
        hierarchy_depth = -1
        for node in self.leaf_nodes:
            if hierarchy_depth == -1:
                hierarchy_depth = self.get_node_depth(node)
            else:
                if hierarchy_depth != self.get_node_depth(node):
                    return False
        return True

    def get_node_depth(self, node):
        """Given a node, get its depth; or in other words, how many levels it has upon him (including the root node)

        :param node: Node we want to check its depth
        :rtype: Node depth count

        """
        if node.parent is not None:
            return 1 + self.get_node_depth(node.parent)
        else:
            return 0

    def get_hierarchy_depth(self):
        """Returns the hierarchy depth (Height)

        :rtype: Hierarchy depth count

        """
        return self.get_node_depth(self.leaf_nodes[0])

    def get_all_nodes_complete_transformation(self):
        """For all the leaf nodes, get their complete list of possible dimensions on the GLG Graph

        :rtype: List of tuples containing all the possible transformations

        """
        nodes_complete_transformation = []
        hierarchy_depth = self.get_hierarchy_depth()
        for node in self.leaf_nodes:
            node_dimension_values = []
            for lvl in range(0, hierarchy_depth+1):
                gen_lvl = self.get_generalization_level_representation(node, lvl)
                node_dimension_values.append(gen_lvl.value)
            nodes_complete_transformation.append(tuple(node_dimension_values))
        return nodes_complete_transformation
