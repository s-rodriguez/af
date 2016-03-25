from af.model.algorithms.BaseKAlgorithm import BaseKAlgorithm
from af.utils import (
    timeit_decorator
)

class Datafly(BaseKAlgorithm):

    def __init__(self, data_config, k):
        BaseKAlgorithm.__init__(self, data_config, k)

    def process(self):
        while self.validate_anonymize_conditions() is not True:
            qi_to_anonymize = self.obtain_qi_most_frequently()
            qi_values = self.anon_db_controller.get_distinct_qi_values(self.anonymization_table, qi_to_anonymize.name)
            dic = {}
            for current_value in qi_values:
                new_value = qi_to_anonymize.transform(current_value, 1)
                if new_value in dic:
                    dic[new_value].append(current_value)
                else:
                    dic[new_value] = [current_value]
            for new_value, old_values in dic.iteritems():
                self.replace_value(qi_to_anonymize.name, new_value, old_values)
