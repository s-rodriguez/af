from af.model.hierarchies.BaseHierarchy import BaseHierarchy, Node
import af.utils as utils


class BaseHierarchyController(object):

    def __init__(self, hierarchy=None):
        self.hierarchy = hierarchy

    def load_hierarchy(self, config_json, attribute_type=str):
        config = utils.load_json(config_json)

        if len(config) > 0:
            self.hierarchy = BaseHierarchy()
            self.hierarchy.populate_nodes(self.hierarchy.root_node, config.values()[0], attribute_type)
        else:
            supression_node = BaseHierarchy.supression_node(None)
            self.hierarchy = BaseHierarchy(supression_node, [])

        return self.hierarchy

    def get_json_representation(self):
        if self.hierarchy is None:
            return {}
        else:
            hierarchy_config = self.hierarchy.hierarchy_representation()
            return utils.get_json_representation(hierarchy_config)
