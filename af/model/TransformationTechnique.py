from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController


class TransformationTechnique(object):

    def __init__(self, name, hierarchy=None):
        self.name = name
        self.hierarchy = hierarchy

    def transform(self, data, lvl=None):
        """Transform original data using its particular technique
        :param data: intended to be modified
        """
        if self.hierarchy is None:
            raise Exception('No hierarchy found')
        return self.hierarchy.transform(data, lvl)

    def transform_leaf_nodes(self, lvl=None):
        if self.hierarchy is None:
            raise Exception('No hierarchy found')
        return self.hierarchy.transform_leaf_nodes(lvl)

    def get_representation(self):
        """Returns the json representation of the techinque"""
        hierarchy_representation = self.hierarchy.hierarchy_representation() if self.hierarchy is not None else {}
        return {
            'name': self.name,
            'hierarchy': hierarchy_representation,
            }

    @staticmethod
    def load_technique(technique_config, data_type):
        name = technique_config['name']
        hierarchy_config = technique_config['hierarchy']

        bhc = BaseHierarchyController()
        bhc.load_hierarchy(hierarchy_config, data_type)

        transformation_technique = TransformationTechnique(name, bhc.hierarchy)
        return transformation_technique
