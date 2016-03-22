import itertools

from af.model.algorithms.BaseKAlgorithm import BaseKAlgorithm


class IncognitoK(BaseKAlgorithm):

    def __init__(self, data_config, k=2):
        BaseKAlgorithm.__init__(self, data_config, k)
        self.glg = None

    def process(self):
        #########################################################################
        ########### CORE ALGORITHM. REVIEW. INTEGRATE. TEST #####################
        #########################################################################
        #lvl = 0
        #glg_nodes = self.glg.get_nodes(lvl=lvl)
        #while glg_nodes is not None:
        #    for node in glg_nodes:
        #        if node is not marked and self.node_checks_k_condition(node):
        #            self.glg.mark_read(node)
        #possible_generalizations = self.glg.get_all_marked_nodes()
        #if possible_generalizations is not None:
        #    generalization_to_use = self.choose_generalization(possible_generalizations)
        #    self.create_anon_table(generalization_to_use)
        #else:
        #    no generalization available to make table anon with that k condition
        #########################################################################
        #########################################################################
        #########################################################################
        pass

    def validate_anonymize_conditions(self):
        pass

    def create_table_hierarchies_star_schema(self):
        for qi_attribute in self.qi_attributes:
            att_dimension_table_name = "{0}_dimensions".format(qi_attribute.name)
            dimensions_amount = qi_attribute.hierarchy.get_hierarchy_depth()
            dimensions = ["{0}0 {1}".format(qi_attribute.name, qi_attribute.basic_type)]
            column_names = ["{0}{1} STRING".format(qi_attribute.name, i) for i in range(1, dimensions_amount+1)]
            dimensions.extend(column_names)

            sql_query = "CREATE TABLE {0} ({1});".format(att_dimension_table_name, ','.join(dimensions))
            list(self.copy_original_db_controller.execute_query(sql_query))

    def insert_values_on_dimension_tables(self):
        pass

    def create_walking_bfs_hierarchy_levels_tree(self):
        qi_info = []
        for att in self.qi_attributes:
            dimensions_amount = att.hierarchy.get_hierarchy_depth()
            qi_info.append((att.name, tuple(range(0, dimensions_amount+1))))

        self.glg = GeneralizationLatticeGraph(qi_info)


class GeneralizationLatticeGraph():

    def __init__(self, qi_info):
        # qi_info example: [('birth', (0, 1)) , ('zip', (0, 1, 2)), ('sex', (0, 1))]
        self.qi_info = qi_info
        self.qi_keys = None
        self.bfs_level_nodes = None
        self.create_bfs_structure()

    def create_bfs_structure(self):
        self.qi_keys = []
        list_of_lvls = []

        for qi_tuple in self.qi_info:
            qi_key, qi_lvls = qi_tuple
            self.qi_keys.append(qi_key)
            list_of_lvls.append(qi_lvls)

        self.bfs_level_nodes = {}

        for subset in itertools.product(*list_of_lvls):
            lvl = sum(subset)
            if lvl not in self.bfs_level_nodes.keys():
                self.bfs_level_nodes[lvl] = []
            self.bfs_level_nodes[lvl].append({'marked': False, 'subset': subset})

    def get_lvl_subsets(self, lvl):
        # Reached the highest possible level
        if lvl not in self.bfs_level_nodes.keys():
            return None
        return {'subsets': self.bfs_level_nodes[lvl], 'qi_keys': self.qi_keys}

    def get_upper_level_nodes(self, node, lvl):
        upper_level_nodes = []
        possible_upper_nodes = self.get_lvl_subsets(lvl)
        if possible_upper_nodes:
            for upper_node in possible_upper_nodes['subsets']:
                condition1 = sum(upper_node['subset'])-sum(node['subset']) == 1
                condition2 = all(0 <= t[1]-t[0] <= 1 for t in zip(node['subset'], upper_node['subset']))
                if all((condition1, condition2)):
                    upper_level_nodes.append(upper_node)
        return upper_level_nodes

    def mark_valid_subset(self, node):
        node['marked'] = True
        current_lvl = sum(node['subset'])
        for upper_node in self.get_upper_level_nodes(node, current_lvl+1):
            self.mark_valid_subset(upper_node)

    def get_processed_lvl_subsets(self, lvl):
        lvl_subsets_raw = self.get_lvl_subsets(lvl)
        if lvl_subsets_raw is None:
            return None
        lvl_subsets_processed = []
        for subset_raw in lvl_subsets_raw['subsets']:
            subset = {}
            for k,v in zip(lvl_subsets_raw['qi_keys'], subset_raw['subset']):
                subset[k] = v
            lvl_subsets_processed.append(subset)
        return lvl_subsets_processed

    @staticmethod
    def test():
        birth_info = ('birth', (0, 1))
        zip_info = ('zip', (0, 1, 2))
        sex_info = ('sex', (0, 1))

        qi_info = (birth_info, zip_info, sex_info)
        glg = GeneralizationLatticeGraph(qi_info)
        print "Get qi keys"
        print glg.qi_keys

        print "\nGet glg representation"
        for lvl, subsets in glg.bfs_level_nodes.iteritems():
            print "Level: "+str(lvl)+": "+str(subsets)

        print "\nGet lvl subsets at request"
        for lvl in range(0, 6):
            print "Level: "+str(lvl)
            print "Subsets :  "+str(glg.get_lvl_subsets(lvl))
            print "(w/keys):  "+str(glg.get_processed_lvl_subsets(lvl))

        print "\nMark all nodes as read"
        glg.mark_valid_subset(glg.bfs_level_nodes[1][1])
        for lvl, subsets in glg.bfs_level_nodes.iteritems():
            print "Level: "+str(lvl)+": "+str(subsets)

if __name__ == "__main__":
    # GLG Test
    GeneralizationLatticeGraph.test()

    #Incognito Test
    #from af.utils import create_full_data_config
    #dc = create_full_data_config.data_config
    #inc = IncognitoK(dc)

    #inc.on_pre_process()
    #inc.create_table_hierarchies_star_schema()
    #inc.create_walking_bfs_hierarchy_levels_tree()

    #for lvl in range(0, 11):
    #    print "Level: "+str(lvl)
    #    print "(w/keys):  "+str(inc.glg.get_processed_lvl_subsets(lvl))
