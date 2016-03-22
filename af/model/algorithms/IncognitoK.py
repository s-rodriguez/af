import itertools

from af.model.algorithms.BaseKAlgorithm import BaseKAlgorithm


class IncognitoK(BaseKAlgorithm):

    def __init__(self, data_config, k=2):
        BaseKAlgorithm.__init__(self, data_config, k)
        self.glg = None
        self.final_generalization = None
        self.k_condition_query = None
        self.replacement_tag = "###REPLACEME###"

    def process(self):
        self.create_table_hierarchies_star_schema()
        self.insert_values_on_dimension_tables()
        self.create_walking_bfs_hierarchy_levels_tree()
        self.create_check_k_condition_query()
        possible_generalizations = self.retrieve_possible_generalizations()
        if len(possible_generalizations) > 0:
            self.final_generalization = self.choose_generalization(possible_generalizations)
            print self.final_generalization
        #    self.create_final_anonymization_table(final_generalization)
        else:
            raise Exception("no generalization available to make table anon with that k condition")

    def validate_anonymize_conditions(self):
        pass

    def create_table_hierarchies_star_schema(self):
        for qi_attribute in self.qi_attributes:
            att_dimension_table_name = "{0}_dimensions".format(qi_attribute.name)
            dimensions_amount = qi_attribute.hierarchy.get_hierarchy_depth()
            dimensions = ["{0}0 {1}".format(qi_attribute.name, qi_attribute.basic_type)]
            
            if dimensions_amount > 0:
                column_names = ["{0}{1} STRING".format(qi_attribute.name, i) for i in range(1, dimensions_amount+1)]
                dimensions.extend(column_names)

            sql_query = "CREATE TABLE {0} ({1});".format(att_dimension_table_name, ','.join(dimensions))
            list(self.copy_original_db_controller.execute_query(sql_query))

    def insert_values_on_dimension_tables(self):
        for qi_attribute in self.qi_attributes:
            att_dimension_table_name = "{0}_dimensions".format(qi_attribute.name)
            amount_of_values = ['?'] * (qi_attribute.hierarchy.get_hierarchy_depth()+1)
            query = "INSERT INTO {0}_dimensions VALUES ({1})".format(qi_attribute.name, ','.join(amount_of_values))
            dimension_values = qi_attribute.hierarchy.get_all_nodes_complete_transformation()
            self.copy_original_db_controller.execute_many(query, dimension_values)

    def create_walking_bfs_hierarchy_levels_tree(self):
        qi_info = []
        for att in self.qi_attributes:
            dimensions_amount = att.hierarchy.get_hierarchy_depth()
            qi_info.append((att.name, tuple(range(0, dimensions_amount+1))))

        self.glg = GeneralizationLatticeGraph(qi_info)

    def create_check_k_condition_query(self):
        table_name = self.data_config.table
        table_initial = self.data_config.table[0:2]
        group_by_clause = []
        sql_query = "SELECT COUNT(*) FROM {0} {1}".format(table_name, table_initial)
        for qi_attribute in self.qi_attributes:
            qi_name = qi_attribute.name
            qi_initial = qi_attribute.name[0:2]
            sql_query += " INNER JOIN {0}_dimensions {1} on {2}.{3} = {4}.{5}0".format(qi_name,
                                                                                          qi_initial,
                                                                                          table_initial,
                                                                                          qi_name,
                                                                                          qi_initial,
                                                                                          qi_name)

            group_by_clause.append("{0}.{1}{2}".format(qi_initial, qi_name, self.replacement_tag))
        sql_query += " GROUP BY {0}".format(', '.join(group_by_clause))

        self.k_condition_query = sql_query

    def retrieve_possible_generalizations(self):
        finished = False
        lvl = 0
        while not finished:
            glg_lvl_subnodes = self.glg.get_lvl_subnodes(lvl)
            if glg_lvl_subnodes is None:
                finished = True
            else:
                for node in glg_lvl_subnodes:
                    if node.marked is False and self.subnode_checks_k_condition(node):
                        self.glg.mark_valid_subnode(node)
                lvl += 1

        possible_generalizations = self.glg.get_marked_nodes()
        return possible_generalizations

    def subnode_checks_k_condition(self, node):
        condition_query = self.k_condition_query.replace('','')
        for key, dimension in zip(node.qi_keys, node.subset):
            condition_query = condition_query.replace('.{0}{1}'.format(key, self.replacement_tag),
                                                      '.{0}{1}'.format(key, dimension))
        
        for row in self.copy_original_db_controller.execute_query(condition_query):
            if int(row[0]) < self.k:
                return False
        return True

    def choose_generalization(self, possible_generalizations):
        # TODO IMPLEMENTE LOGIC TO CHOOSE
        return possible_generalizations[0]

    def create_final_anonymization_table(self, final_generalization):
        pass


class GLGNode():
    def __init__(self, subset, glg_lvl, qi_keys, marked=False):
        self.subset = subset
        self.glg_lvl = glg_lvl
        self.qi_keys = qi_keys
        self.marked = marked

    def __repr__(self):
        return str({'subset': self.subset, 'marked': self.marked})
        

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
            self.bfs_level_nodes[lvl].append(GLGNode(subset=subset, glg_lvl=lvl, qi_keys=self.qi_keys, marked=False))

    def get_lvl_subnodes(self, lvl):
        # Reached the highest possible level
        if lvl not in self.bfs_level_nodes.keys():
            return None
        return self.bfs_level_nodes[lvl]

    def get_upper_level_nodes(self, node, lvl):
        upper_level_nodes = []
        possible_upper_nodes = self.get_lvl_subnodes(lvl)
        if possible_upper_nodes:
            for upper_node in possible_upper_nodes:
                condition1 = sum(upper_node.subset)-sum(node.subset) == 1
                condition2 = all(0 <= t[1]-t[0] <= 1 for t in zip(node.subset, upper_node.subset))
                if all((condition1, condition2)):
                    upper_level_nodes.append(upper_node)
        return upper_level_nodes

    def mark_valid_subnode(self, node):
        node.marked = True
        current_lvl = sum(node.subset)
        for upper_node in self.get_upper_level_nodes(node, current_lvl+1):
            self.mark_valid_subnode(upper_node)

    def get_marked_nodes(self, marked=True):
        marked_nodes = []
        lvl = 0
        finished = False
        
        while not finished:
            nodes = self.get_lvl_subnodes(lvl)
            if nodes is None:
                finished = True
            else:    
                marked_nodes.extend([node for node in nodes if node.marked == marked])
                lvl += 1
        return marked_nodes

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
            print "Subsets :  "+str(glg.get_lvl_subnodes(lvl))

        print "\nMark all nodes as read"
        glg.mark_valid_subnode(glg.bfs_level_nodes[1][1])
        for lvl in range(0, 6):
            print "Level: "+str(lvl)
            print "Subsets :  "+str(glg.get_lvl_subnodes(lvl))

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
