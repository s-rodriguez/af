from af.controller.data.SqliteController import SqliteController
from af import utils

class BaseAlgorithm(object):

    def __init__(self, data_config):
        self.data_config = data_config
        self.anonymization_table = None
        self.input_table = None
        self.qi_attributes = data_config.attributes_list
        self.db_controller = SqliteController(utils.get_anonymization_db_location())

    def anonymize(self):
        pass

    def validate_anonymize_conditions(self):
        pass

    def on_pre_process(self):
        pass

    def on_post_process(self):
        pass

    def obtain_quasi_identifier_frequencies(self):
        for value in self.db_controller.get_frequency_of_qi_attributes(self.anonymization_table, self.qi_attributes):
            yield value

    def obtain_qi_most_frequently(self):
        qi_most_frequently = None
        qi_most_frequently_count = 0
        for qi in self.qi_attributes:
            frequency = self.db_controller.get_count_of_distinct_qi_values(qi)
            if (qi_most_frequently is None) or (frequency > qi_most_frequently_count):
                qi_most_frequently = qi
                qi_most_frequently_count = frequency
        return qi_most_frequently

    def replace_value(self, qi, new_value, old_value):
        self.db_controller.replace_qi_value(self.anonymization_table, qi, new_value, old_value)
