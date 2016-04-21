import logging

from af.model.algorithms.IncognitoK import IncognitoK
from af.utils import (
    timeit_decorator,
    PRIVACY_TYPE_SENSITIVE,
    L_PRIVACY_MODEL)


class IncognitoL(IncognitoK):
    """Incognito-L Algorithm implementation.
    Extends the IncognitoK algorithm implementation

    """
    PRIVACY_MODEL = L_PRIVACY_MODEL
    ALGORITHM_NAME = 'Incognito L'

    def __init__(self, data_config, k=3, l=2, optimized_processing=False):
        IncognitoK.__init__(self, data_config, k, optimized_processing)
        self.logger = logging.getLogger('algorithms.IncognitoL')

        self.l = l
        self.l_condition_query = None
        self.sensitive_att_name = None

        self.load_sensitive_attribute()

    def validate_arguments(self):
        """Validates the general arguments, like the data config and the k value (Using the parent classes), and also validates the L value

        """
        IncognitoK.validate_arguments(self)
        try:
            self.l = int(self.l)
        except:
            error_message = "L param must be an int"
            self.logger.error(error_message)
            raise Exception(error_message)

        if self.l < 2 or self.l > self.k:
            error_message = "Invalid l param"
            self.logger.error(error_message)
            raise Exception(error_message)

    def load_sensitive_attribute(self):
        """The L-diversity model is based on a sensitive attribute. Select from the data configuration, which is the sensitive attribute to be taken into account.

        """
        sensitive_att = self.data_config.get_privacy_type_attributes_list(PRIVACY_TYPE_SENSITIVE)
        if len(sensitive_att) != 1:
            error_message = "IncognitoL handles ony 1 sensitive attribute"
            self.logger.error(error_message)
            raise Exception(error_message)
        self.sensitive_att_name = sensitive_att[0].name

    @timeit_decorator
    def create_condition_queries(self):
        """Create the K and L condition queries to use during the anonymization process

        """
        self.create_check_k_condition_query()
        self.create_check_l_condition_query()

    @timeit_decorator
    def create_check_l_condition_query(self):
        """Create the L condition query, which is based on the sensitive attribute and the amount of appearances on a table_name

        """
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
        """Check all the model conditions to determine if the node given accomplishes the requirements necessary to be considered a possible generalization

        :param node: GLGNode instance to be used
        :rtype: Boolean indicating if the node can be used a generalization for the anonymization process

        """
        k_condition = self.subnode_checks_k_condition(node)
        if k_condition:
            return self.subnode_checks_l_condition(node)
        else:
            return k_condition

    def subnode_checks_l_condition(self, node):
        """Specific method that checks the L condition given a node

        :param node: GLGNode instance to be used
        :rtype: Boolean indicating if the L condition has been met or not.

        """
        condition_query = self.l_condition_query.replace('','')
        for key, dimension in zip(node.qi_keys, node.subset):
            condition_query = condition_query.replace('.{0}{1}'.format(key, self.replacement_tag),
                                                      '.{0}{1}'.format(key, dimension))

        for row in self.anon_db_controller.execute_query(condition_query):
            if int(row[0]) < self.l:
                return False
        return True

    def on_post_process(self):
        """After the anonymization process has ended, save particular information of it

        """
        self.additional_anonymization_info[2] = ('Model Conditions', "K: {0}   L: {1}".format(self.k, self.l))
        self.additional_anonymization_information()
