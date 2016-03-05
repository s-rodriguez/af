from af.model.hierarchies.BaseHierarchy import BaseHierarchy, Node


class BaseHierarchyController(object):

    def __init__(self, hierarchy=None):
        self.hierarchy = hierarchy

    def load_hierarchy(self, config, attribute_type=str):

        new_hierarchy = BaseHierarchy()
        if isinstance(config, dict):
            new_hierarchy.populate_nodes(new_hierarchy.root_node, config.values()[0], attribute_type)

        self.hierarchy = new_hierarchy

        return self.hierarchy

    def get_hierarchy_representation(self):
        if self.hierarchy is None:
            return None
        else:
            hierarchy_config = self.hierarchy.hierarchy_representation()
            return hierarchy_config
