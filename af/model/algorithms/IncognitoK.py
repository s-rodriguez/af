import logging
import random

from statistics import median

from af.model.algorithms.BaseKAlgorithm import BaseKAlgorithm
from af.model.algorithms.GeneralizationLatticeGraph import  GeneralizationLatticeGraph
from af.utils import (
    ANONYMIZED_DATA_TABLE,
    timeit_decorator,
    K_PRIVACY_MODEL
)


class IncognitoK(BaseKAlgorithm):
    """Incognito-K Algorithm implementation.
    It is mainly based on heavy join queries across tables that contains dimensions of qi attributes and different values

    """
    PRIVACY_MODEL = K_PRIVACY_MODEL
    ALGORITHM_NAME = 'Incognito K'

    def __init__(self, data_config, k=2, optimized_processing=False):
        BaseKAlgorithm.__init__(self, data_config, k, optimized_processing)
        self.logger = logging.getLogger('algorithms.IncognitoK')
        self.k_condition_query = None
        self.anonymization_table = ANONYMIZED_DATA_TABLE
        self.glg = None
        self.final_generalization = None
        self.possible_generalizations = None
        self.best_minimal_generalizations = None
        self.replacement_tag = "###REPLACEME###"

    @timeit_decorator
    def process(self):
        """The main core algorithm to anonymize using the Incognito-K implementation

        """
        self.create_table_hierarchies_star_schema()
        self.insert_values_on_dimension_tables()
        self.create_walking_bfs_hierarchy_levels_tree()
        self.create_condition_queries()
        self.possible_generalizations = self.retrieve_possible_generalizations()
        if len(self.possible_generalizations) > 0:
            self.final_generalization = self.choose_generalization(self.possible_generalizations)
            self.dump_anonymized_data()
        else:
            error_message = "No generalization available to make table anon with that k condition"
            self.logger.error(error_message)
            raise Exception(error_message)

    @timeit_decorator
    def create_table_hierarchies_star_schema(self):
        """Create the table hierarchies star schema for the different quasi-identifiers of the data config.
        Apart from the table, create an index on the first column dimension (As it is the one that will be used for the join queries)

        """
        self.logger.info("Creating table hierarchies star schema...")
        for qi_attribute in self.qi_attributes:
            att_dimension_table_name = "{0}_dimensions".format(qi_attribute.name)
            dimensions_amount = qi_attribute.hierarchy.get_hierarchy_depth()
            dimensions = ["{0}0 {1}".format(qi_attribute.name, qi_attribute.basic_type)]

            if dimensions_amount > 0:
                column_names = ["{0}{1} STRING".format(qi_attribute.name, i) for i in range(1, dimensions_amount+1)]
                dimensions.extend(column_names)

            sql_query = "CREATE TABLE {0} ({1});".format(att_dimension_table_name, ','.join(dimensions))
            list(self.anon_db_controller.execute_query(sql_query))

            index_query = "CREATE INDEX {0}_index ON {1} ({2}0);".format(qi_attribute.name[0:2],
                                                                        att_dimension_table_name,
                                                                        qi_attribute.name)
            list(self.anon_db_controller.execute_query(index_query))

    @timeit_decorator
    def insert_values_on_dimension_tables(self):
        """For each of the quasi-identifiers attributes, insert their distinct dimensions values in their hierarchy dimension table.

        """
        self.logger.info("Inserting values on dimension tables...")
        for qi_attribute in self.qi_attributes:
            amount_of_values = ['?'] * (qi_attribute.hierarchy.get_hierarchy_depth()+1)
            query = "INSERT INTO {0}_dimensions VALUES ({1})".format(qi_attribute.name, ','.join(amount_of_values))
            dimension_values = qi_attribute.hierarchy.get_all_nodes_complete_transformation()
            self.anon_db_controller.execute_many(query, dimension_values)

    @timeit_decorator
    def create_walking_bfs_hierarchy_levels_tree(self):
        """The algorithm uses a GeneralizationLatticeGraph as a mean to travel the different combinations to be tested.
        Create the GLG based on all the quasi-identifiers information and save it.

        """
        self.logger.info("Creating Generalization Lattice Graph...")
        qi_info = []
        for att in self.qi_attributes:
            dimensions_amount = att.hierarchy.get_hierarchy_depth()
            qi_info.append((att.name, tuple(range(0, dimensions_amount+1))))

        self.glg = GeneralizationLatticeGraph(qi_info)

    @timeit_decorator
    def create_condition_queries(self):
        """Create all the necessary condition queries to be used afterwards during the process stage

        """
        self.create_check_k_condition_query()

    @timeit_decorator
    def create_check_k_condition_query(self):
        """Creates the specific K condition query that is in charge of validating if a certain subset of dimensions validates the K-model condition

        """
        self.logger.info("Forming k condition query...")
        table_name = self.data_config.table
        table_initial = self.data_config.table[0:2]

        sql_query = "SELECT COUNT(*) FROM {0} {1}".format(table_name, table_initial)

        inner_join_query, group_by_query = self._get_inner_join_and_group_by_query_parts(table_initial)

        sql_query += inner_join_query
        sql_query += group_by_query

        self.k_condition_query = sql_query

    @timeit_decorator
    def _get_inner_join_and_group_by_query_parts(self, table_initial):
        """Every query depends on a massive inner join between the hierary dimensions tables (Star schema).
        Given all the quasi-identifiers attributes, create a generic inner join and group by query

        :rtype: Query string

        """
        inner_join_query = ""
        group_by_clause = []

        for qi_attribute in self.qi_attributes:
            qi_name = qi_attribute.name
            qi_initial = qi_attribute.name[0:2]
            inner_join_query += " INNER JOIN {0}_dimensions {1} on {2}.{3} = {4}.{5}0".format(qi_name,
                                                                                          qi_initial,
                                                                                          table_initial,
                                                                                          qi_name,
                                                                                          qi_initial,
                                                                                          qi_name)

            group_by_clause.append("{0}.{1}{2}".format(qi_initial, qi_name, self.replacement_tag))

        group_by_query = " GROUP BY {0}".format(', '.join(group_by_clause))

        return (inner_join_query, group_by_query)

    @timeit_decorator
    def retrieve_possible_generalizations(self):
        """Using the GLG as the BFS tree, travel it, and use the different subsets the nodes give to check if they validate the K-model condition.
        Save all those that can be used a possible generalizations and return them

        :rtype: List of GLGNodes that can be used to generalize the current table

        """
        self.logger.info("Retrieving all possible generalizations...")
        finished = False
        lvl = 0
        possible_generalizations = None

        while not finished:
            glg_lvl_subnodes = self.glg.get_lvl_subnodes(lvl)
            if glg_lvl_subnodes is None:
                finished = True
            else:
                for node in glg_lvl_subnodes:
                    if node.marked is False and self.checks_model_conditions(node):
                        if self.optimized_processing:
                            possible_generalizations = [node]
                            finished = True
                            break
                        self.glg.mark_valid_subnode(node)
                lvl += 1

        if not self.optimized_processing:
            possible_generalizations = self.glg.get_marked_nodes()

        return possible_generalizations

    def checks_model_conditions(self, node):
        """Call every method that contains a model validation.
        For this particular case, only the k condition. It can be re implemented for algorithms that inherit from this class

        :param node: GLGNode to use
        :rtype: Boolean depending if all the conditions have been met or not.

        """
        return self.subnode_checks_k_condition(node)

    def subnode_checks_k_condition(self, node):
        """Method that will query the table given a certain node to check if it's subset validates the K-model condition_query

        :param node: GLGNode to use
        :rtype: True if the k condition has been met, False otherwise

        """
        condition_query = self.k_condition_query.replace('','')
        for key, dimension in zip(node.qi_keys, node.subset):
            condition_query = condition_query.replace('.{0}{1}'.format(key, self.replacement_tag),
                                                      '.{0}{1}'.format(key, dimension))
        for row in self.anon_db_controller.execute_query(condition_query):
            if int(row[0]) < self.k:
                return False
        return True

    def normal_filter(self, list_to_filter, filter_method):
        """Auxiliary method that will filter a list given a filter method, and returns the filtered value

        :param list list_to_filter: List to be filtered
        :param filter_method: A method that receives 2 subsets and decide how to filter based on its own conditions
        :rtype: List filtered by the filter_method

        """
        filtered_list = []
        for item in list_to_filter:
            if len(filtered_list) == 0 or filter_method(item.subset, filtered_list[0].subset) == -1:
                filtered_list = [item]
            elif filter_method(item.subset, filtered_list[0].subset) == 0:
                filtered_list.append(item)
        return filtered_list

    def weighted_filter(self, list_to_filter):
        """Specific filter that will try to reduce a certain list of filters, using the subset weights as key filter

        :param list list_to_filter: List intended to be filtered
        :rtype: A filtered by attribute weight list

        """
        filtered_list = []
        weights = dict((att.name, att.weight) for att in self.qi_attributes)

        def item_weight(item):
            item_weight_sum = 0
            for name, lvl in zip(item.qi_keys, item.subset):
                item_weight_sum += lvl/(weights[name]+0.0)
            return item_weight_sum

        for item in list_to_filter:
            if len(filtered_list) == 0 or item_weight(item) < item_weight(filtered_list[0]):
                filtered_list = [item]
            elif item_weight(item) == item_weight(filtered_list[0]):
                filtered_list.append(item)
        return filtered_list

    @timeit_decorator
    def choose_generalization(self, possible_generalizations):
        """Given a list of possible generalizations that met the conditions of the model, decide which is the best one to use.

        :param list possible_generalizations: List of GLGNodes containing possible generalizations to be used.
        :rtype: GLGNode consider to be the best generalization to use

        """
        self.logger.info("Choosing the best generalization from the possible ones...")

        filters = [
            lambda x, y: -1 if sum(x) < sum(y) else (0 if sum(x) == sum(y) else 1),  # lower_levels
            lambda x, y: -1 if median(x) < median(y) else (0 if median(x) == median(y) else 1)  # lowest_median
        ]

        self.best_minimal_generalizations = possible_generalizations
        for f in filters:
            self.best_minimal_generalizations = self.normal_filter(self.best_minimal_generalizations, f)
            if len(self.best_minimal_generalizations) == 1:
                break

        if len(self.best_minimal_generalizations) > 1:
            # try to filter using the attributes weights
            self.best_minimal_generalizations = self.weighted_filter(self.best_minimal_generalizations)

        best_minimal_generalization = random.choice(self.best_minimal_generalizations)

        return best_minimal_generalization

    @timeit_decorator
    def dump_anonymized_data(self):
        """Once the anonymization process has decided which generalization subset to use for the quasi-identifiers attributes, the next step is to dump the anonymized data using it.

        """
        self.logger.info("Dumping anonymized data with dimensions: {0}...".format(str(self.final_generalization)))

        # CREATE TABLE TO STORE ANONYMIZED DATA
        table_name = ANONYMIZED_DATA_TABLE
        columns = self.anon_db_controller.table_columns_info(self.data_config.table)

        create_table_query = "CREATE TABLE {0} ({1});".format(table_name, ', '.join(columns))
        list(self.anon_db_controller.execute_query(create_table_query))

        # INSERT DATA INTO TABLE
        original_table_name = self.data_config.table
        original_table_initial = self.data_config.table[0:2]

        qi_dimensions = dict((att_name, att_dimension) for att_name, att_dimension in zip(self.final_generalization.qi_keys, self.final_generalization.subset))

        select_attributes = []
        for att_name in columns:
            if att_name not in qi_dimensions.keys():
                select_attributes.append("{0}.{1}".format(original_table_initial, att_name))
            else:
                dimension = qi_dimensions[att_name]
                select_attributes.append("{0}.{1}{2}".format(att_name[0:2], att_name, dimension))

        insert_query = "INSERT INTO {0} ({1})".format(table_name, ', '.join(columns))
        insert_query += " SELECT {0} FROM {1} {2}".format(', '.join(select_attributes), original_table_name, original_table_initial)

        inner_join_query, _ = self._get_inner_join_and_group_by_query_parts(original_table_initial)
        insert_query += inner_join_query

        list(self.anon_db_controller.execute_query(insert_query))

    def additional_anonymization_information(self):
        """Add particular anonymization information of the process to the dictionary of additional information

        """
        selected_hierarchy_levels = dict((key, dimension) for key, dimension in zip(self.final_generalization.qi_keys, self.final_generalization.subset))

        self.additional_anonymization_info[3] = ('Selected Hierarchy Levels', selected_hierarchy_levels)

        def possible_generalizations_info(generalizations_list):
            possible_generalizations = []
            for possible_gen in generalizations_list:
                possible_generalizations.append(str(dict((key, dimension) for key, dimension in zip(possible_gen.qi_keys, possible_gen.subset))))
            return '\n'.join(possible_generalizations)

        if len(self.best_minimal_generalizations) > 1:
            self.additional_anonymization_info[4] = ('Best Minimal Hierarchy Levels', possible_generalizations_info(self.best_minimal_generalizations))

        if len(self.possible_generalizations) > 1:
            self.additional_anonymization_info[5] = ('Other Possible Hierarchy Levels', possible_generalizations_info(self.possible_generalizations))

    def on_post_process(self):
        """After the anonymization process has ended, save particular information of it

        """
        self.additional_anonymization_info[2] = ('Model Conditions', "K: {0}".format(self.k))
        self.additional_anonymization_information()
