from af.model.hierarchies.BaseHierarchy import BaseHierarchy
from af.model.hierarchies.Node import Node
from af.utils import mapping_types
from af.utils import (
    HIERARCHY_TYPE_GENERALIZATION,
    HIERARCHY_TYPE_SUPPRESSION,
)
from af.model.AfManager import AfManager


class BaseHierarchyController(object):
    """Class that is intended to be used for the load and save of BaseHierarchy instances

    """
    def __init__(self, hierarchy=None):
        self.hierarchy = hierarchy

    def load_hierarchy(self, config, attribute_type='string'):
        """Given a configuration, it loads the hierarchy that was saved.

        :param config: Configuration in the form of a dictionary that associates values with its parent level values. If its a string, then it is assumed that the hierarchy was a suprression hierarchy.
        :param string attribute_type: The specific type of the attribute.

        """
        attribute_type = mapping_types(attribute_type)
        new_hierarchy = BaseHierarchy()
        if isinstance(config, dict):
            hierarchy_representation = config['hierarchy_representation']
            hierarchy_type = config['hierarchy_type']
            new_hierarchy.populate_nodes(new_hierarchy.root_node, hierarchy_representation.values()[0], attribute_type)
            new_hierarchy.hierarchy_type = hierarchy_type
            if new_hierarchy.validate_hierarchy_depth() is not True:
                raise Exception("Load hierarchy failed: all leaf nodes must have same depth")

        self.hierarchy = new_hierarchy

        return self.hierarchy

    def get_hierarchy_representation(self):
        """Returns the representation of the hierarchy (If it exists)

        :rtype: dict

        """
        if self.hierarchy is None:
            return None
        else:
            hierarchy_config = self.hierarchy.hierarchy_representation()
            return hierarchy_config

    @staticmethod
    def create_hierarchy_from_list_of_values(list_of_values):
        """Given a list of lists, containing the information about a hierarchy,
        create the hierarchy, and return it

        :param list_of_values: List containing all the values of the hierarchies, per rows
        :rtype: BaseHierarchy instance

        """
        new_hierarchy = BaseHierarchy(HIERARCHY_TYPE_GENERALIZATION)

        for row in list_of_values:
            BaseHierarchyController._add_new_node(new_hierarchy, new_hierarchy.root_node, row)

        return new_hierarchy

    @staticmethod
    def create_suppression_hierarchy():
        """Create a suppression hierarchy and return it

        :rtype: BaseHierarchy instance

        """
        new_hierarchy = BaseHierarchy(HIERARCHY_TYPE_SUPPRESSION)

        return new_hierarchy

    def create_automatic_dimension_hierarchy(self, automatic_dimension_name, automatic_dimension_args, list_of_values, attribute_type=str):
        """Given the automatic dimension name, his arguments, the attribute type and the list of values
        create the suppression hierarchy.

        :param automatic_dimension_name: Automatic dimension name used to build the hierarchy
        :param automatic_dimension_args: List of particular arguments the automtic dimension needs
        :param list_of_values: List containing all the values of the hierarchies, per rows
        :param attribute_type: Attribute type (int ,str or date)


        :rtype: BaseHierarchy instance

        """
        af_manager = AfManager()
        automatic_dimension = af_manager.get_automatic_dimension_instance(automatic_dimension_name, list_of_values, automatic_dimension_args)
        automatic_dimension_representation = automatic_dimension.create_dimensions()
        automatic_dimension_dict = {'hierarchy_type': HIERARCHY_TYPE_SUPPRESSION,
                                     'hierarchy_representation': automatic_dimension_representation}

        suppression_hierarchy = self.load_hierarchy(automatic_dimension_dict, attribute_type)
        return suppression_hierarchy

    @staticmethod
    def _add_new_node(hierarchy, parent_node, values):
        if len(values) > 0:
            value = values.pop()
            node = parent_node.get_leaf_node(value)
            if node is None:
                node = Node(value)
                hierarchy.add_node(parent_node, node)

            BaseHierarchyController._add_new_node(hierarchy, node, values)
