from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController
from af.utils import (
    BASIC_TYPE_STRING,
    PRIVACY_TYPE_NON_SENSITIVE,
    PRIVACY_TYPE_QI,
)


class Attribute(object):
    """Class that models an attribute of a table.

    """
    def __init__(self, name=None, basic_type=BASIC_TYPE_STRING, privacy_type=PRIVACY_TYPE_NON_SENSITIVE, hierarchy=None, weight=1):
        self.name = name
        self.basic_type = basic_type
        self.privacy_type = privacy_type
        self.weight = weight
        self.hierarchy = None
        self.set_hierarchy(hierarchy)

    def get_representation(self):
        """Returns the representation of the attribute

        :rtype: Attribute representation in a dictionary form

        """
        return {
            'name': self.name,
            'basic_type': self.basic_type,
            'privacy_type': self.privacy_type,
            'weight': self.weight,
            'hierarchy': self.get_hierarchy_representation()
        }

    def load_config(self, config_dict):
        """Given a configuration, it loads the attribute based on the saved data.

        :param dict config_dict: Dictionary containing information about the attribute

        """
        self.name = config_dict['name']
        self.basic_type = config_dict['basic_type']
        self.privacy_type = config_dict['privacy_type']
        self.weight = config_dict['weight']
        self.set_hierarchy(config_dict['hierarchy'])

    def get_hierarchy_representation(self):
        """Returns the representation of the attribute hierarchy, if any

        :rtype: Dictionary representation of hierarchy (None if no hierarchy associated to the attribute)

        """
        if self.hierarchy is not None:
            return self.hierarchy.hierarchy_representation()
        else:
            return None

    def set_hierarchy(self, hierarchy_config):
        """Given a hierarchy configuration, load it and save it to the attribute

        :param dict hierarchy_config: hierarchy configuration in the form of a dictionary

        """
        self.hierarchy = None
        if hierarchy_config is not None:
            self.hierarchy = BaseHierarchyController().load_hierarchy(hierarchy_config, self.basic_type)

    def transform(self, data, lvl=None):
        """Transform original data using its particular hierarchy

        :param string data: intended to be modified
        :param int lvl: Level to generalize
        :rtype: attribute value generalized to the level required

        """
        if self.hierarchy is None:
            raise Exception('No hierarchy found')
        return self.hierarchy.transform(data, lvl)

    def transform_leaf_nodes(self, lvl=1):
        """Get the full transformation of all the leaf nodes for the attribute

        :param int lvl: Level to generalize
        :rtype: List of transformed values for all leaf nodes

        """
        if self.hierarchy is None:
            raise Exception('No hierarchy found')
        return self.hierarchy.transform_leaf_nodes(lvl)

    def __repr__(self):
        return "{0} - [{1}-{2}] ({3})".format(self.name, self.basic_type, self.privacy_type, self.weight)

    def is_qi_attribute(self):
        """Checks if it is a qi attribute

        :rtype: True if it is a QI attribute, False if not

        """
        return self.privacy_type == PRIVACY_TYPE_QI
