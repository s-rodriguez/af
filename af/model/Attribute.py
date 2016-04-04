from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController


class Attribute(object):

    def __init__(self, name=None, basic_type='string', privacy_type=None, hierarchy_config=None, weight=1):
        self.name = name
        self.basic_type = basic_type
        self.privacy_type = privacy_type
        self.weight = weight
        self.hierarchy = None
        self.set_hierarchy(hierarchy_config)

    def get_representation(self):
        return {
            'name': self.name,
            'basic_type': self.basic_type,
            'privacy_type': self.privacy_type,
            'weight': self.weight,
            'hierarchy': self.get_hierarchy_representation()
        }

    def load_config(self, config_dict):
        self.name = config_dict['name']
        self.basic_type = config_dict['basic_type']
        self.privacy_type = config_dict['privacy_type']
        self.weight = config_dict['weight']
        self.set_hierarchy(config_dict['hierarchy'])

    def get_hierarchy_representation(self):
        if self.hierarchy is not None:
            return self.hierarchy.hierarchy_representation()
        else:
            return None

    def set_hierarchy(self, hierarchy_config):
        self.hierarchy = None
        if hierarchy_config is not None:
            self.hierarchy = BaseHierarchyController().load_hierarchy(hierarchy_config, self.basic_type)

    def transform(self, data, lvl=None):
        """Transform original data using its particular hierarchy
        :param data: intended to be modified
        """
        if self.hierarchy is None:
            raise Exception('No hierarchy found')
        return self.hierarchy.transform(data, lvl)

    def transform_leaf_nodes(self, lvl=1):
        if self.hierarchy is None:
            raise Exception('No hierarchy found')
        return self.hierarchy.transform_leaf_nodes(lvl)

    def __repr__(self):
        return "{0} - [{1}-{2}] ({3})".format(self.name, self.basic_type, self.privacy_type, self.weight)
