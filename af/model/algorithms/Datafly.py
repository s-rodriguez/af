import logging

from af.model.algorithms.BaseKAlgorithm import BaseKAlgorithm


class Datafly(BaseKAlgorithm):

    def __init__(self, data_config, k):
        BaseKAlgorithm.__init__(self, data_config, k)
        self.logger = logging.getLogger('algorithms.Datafly')
        self.iteration = 0

    def process(self):
        while self.validate_anonymize_conditions() is not True:
            self.iteration += 1
            self.logger.info("Datafly {0} iteration...".format(str(self.iteration)))
            qi_to_anonymize = self.obtain_qi_most_frequently()
            qi_values = self.anon_db_controller.get_distinct_qi_values(self.anonymization_table, qi_to_anonymize.name)
            values_to_update_dic = {}
            for current_value in qi_values:
                new_value = qi_to_anonymize.transform(current_value, 1)
                if new_value in values_to_update_dic:
                    values_to_update_dic[new_value].append(current_value)
                else:
                    values_to_update_dic[new_value] = [current_value]
            self.update_qi_values(qi_to_anonymize, values_to_update_dic)
