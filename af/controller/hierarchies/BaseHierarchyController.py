from af.model.hierarchies.BaseHierarchy import BaseHierarchy, Node
from af.utils import mapping_types


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
            new_hierarchy.populate_nodes(new_hierarchy.root_node, config.values()[0], attribute_type)
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
