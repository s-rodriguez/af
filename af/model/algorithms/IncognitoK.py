import itertools

from af.model.algorithms.BaseKAlgorithm import BaseKAlgorithm


class IncognitoK(BaseKAlgorithm):

    def __init__(self, data_config):
        BaseKAlgorithm.__init__(self, data_config)
        self.db_original_copy_controller = SqliteController()

    def anonymize(self):
        self.on_pre_process()
        # while self.validate_anonymize_conditions(self.attributes) is not True:
        #     qi_to_anonymize = self.obtain_qi_most_frequently()
        #     # qi_to_anonymize.transformation_technique.transform(...
        self.on_post_process()


    def validate_anonymize_conditions(self):
        pass

    def create_walking_bfs_hierarchy_levels_tree(self):
        pass

    def create_table_hierarchies_star_schema(self):
        pass





class GeneralizationLatticeGraph():

    def __init__(self, list_of_lvls):
        self.list_of_lvls = list_of_lvls
        self.bfs_level_nodes = None
        self.create_bfs_structure()

    def create_bfs_structure(self):
        self.bfs_level_nodes = {}

        for subset in itertools.product(*self.list_of_lvls):
            lvl = sum(subset)
            if lvl not in self.bfs_level_nodes.keys():
                self.bfs_level_nodes[lvl] = []
            self.bfs_level_nodes[lvl].append(subset)

    def upper_level_nodes(self, current_node):
        condition1 = sum(next_node)-sum(current_node) == len(current_node)-1
        condition2 = all(tuple[1]-tuple[0] <= 1 for tuple in zip(next_node, current_node))

    @staticmethod
    def test():
        birth_lvls = [0, 1]
        zip_lvls = [0, 1, 2]
        sex_lvls = [0, 1]
        
        list_of_lvls = (birth_lvls, sex_lvls, zip_lvls)
        glg = GeneralizationLatticeGraph(list_of_lvls)
        for lvl, subsets in glg.bfs_level_nodes.iteritems():
            print "Level: "+str(lvl)+": "+str(subsets)


if __name__ == "__main__":
    GeneralizationLatticeGraph.test()
