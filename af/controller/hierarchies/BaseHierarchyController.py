from af.model.hierarchies.BaseHierarchy import BaseHierarchy, Node
import af.utils as utils


class BaseHierarchyController(object):

    def __init__(self, hierarchy=None):
        self.hierarchy = hierarchy

    def load_hierarchy(self, config_json, attribute_type=str):
        config = utils.load_json(config_json)

        new_hierarchy = BaseHierarchy()
        if isinstance(config, dict):
            new_hierarchy.populate_nodes(new_hierarchy.root_node, config.values()[0], attribute_type)

        self.hierarchy = new_hierarchy

        return self.hierarchy

    def get_json_representation(self):
        if self.hierarchy is None:
            return None
        else:
            hierarchy_config = self.hierarchy.hierarchy_representation()
            return utils.get_json_representation(hierarchy_config)
