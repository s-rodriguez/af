from af.model.hierarchies.BaseHierarchy import BaseHierarchy, Node
import af.utils as utils
class BaseHierarchyController(object):

    def __init__(self, hierarchy=None):
        self.hierarchy = hierarchy

    def load_hierarchy(self, config):
        root_node = Node(config.keys()[0])
        self.hierarchy = BaseHierarchy(root_node, [])

        self.hierarchy.populate_nodes(root_node, config.values()[0])

        return self.hierarchy

    def get_json_representation(self):
        if self.hierarchy is None:
            return {}
        else:
            hierarchy_config = self.hierarchy.hierarchy_representation()
            return utils.get_json_representation(hierarchy_config)
