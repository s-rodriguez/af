import logging

from af.model.algorithms.IncognitoK import IncognitoK
from af.utils import (
    timeit_decorator,
    PRIVACY_TYPE_SENSITIVE,
)


class IncognitoL(IncognitoK):

    def __init__(self, data_config, k=3, l=2, look_for_all=False):
        IncognitoK.__init__(self, data_config, k, look_for_all)
        self.logger = logging.getLogger('algorithms.IncognitoL')

        self.validate_arguments(k, l)

        self.l = l
        self.l_condition_query = None
        self.sensitive_att_name = None

        self.load_sensitive_attribute()

    def validate_arguments(self, k, l):
        if l < 2 or l > k:
            error_message = "Invalid l param"
            self.logger.error(error_message)
            raise Exception(error_message)

    def load_sensitive_attribute(self):
        sensitive_att = self.data_config.get_privacy_type_attributes_list(PRIVACY_TYPE_SENSITIVE)
        if len(sensitive_att) != 1:
            error_message = "IncognitoL handles ony 1 sensitive attribute"
            self.logger.error(error_message)
            raise Exception(error_message)
        self.sensitive_att_name = sensitive_att[0].name

    @timeit_decorator
    def create_condition_queries(self):
        self.create_check_k_condition_query()
        self.create_check_l_condition_query()

    @timeit_decorator
    def create_check_l_condition_query(self):
        self.logger.info("Forming l condition query...")
        table_name = self.data_config.table
        table_initial = self.data_config.table[0:2]

        sql_query = "SELECT COUNT(DISTINCT {0}.{1}) FROM {2} {3}".format(table_initial,
                                                                         self.sensitive_att_name,
                                                                         table_name,
                                                                         table_initial)

        inner_join_query, group_by_query = self._get_inner_join_and_group_by_query_parts(table_initial)

        sql_query += inner_join_query
        sql_query += group_by_query

        self.l_condition_query = sql_query

    def checks_model_conditions(self, node):
        k_condition = self.subnode_checks_k_condition(node)
        if k_condition:
            return self.subnode_checks_l_condition(node)
        else:
            return k_condition

    @timeit_decorator
    def subnode_checks_l_condition(self, node):
        condition_query = self.l_condition_query.replace('','')
        for key, dimension in zip(node.qi_keys, node.subset):
            condition_query = condition_query.replace('.{0}{1}'.format(key, self.replacement_tag),
                                                      '.{0}{1}'.format(key, dimension))

        for row in self.anon_db_controller.execute_query(condition_query):
            if int(row[0]) < self.l:
                return False
        return True
