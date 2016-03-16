from af.controller.data.SqliteController import SqliteController
from af import utils

class BaseAlgorithm(object):

    def __init__(self, data_config):
        self.data_config = data_config
        self.anonymization_table = None
        self.input_table = None
        self.attributes = data_config.attributes_list
        self.db_controller = SqliteController(utils.get_anonymization_db_location())

    def anonymize(self):
        pass

    def validate_anonymize_conditions(self):
        pass

    def input_preprocessing(self):
        pass

    def read_input_table(self):
        # this method should be implemented here
        pass

    def write_ouput_table(self):
        # this method should be implemented here
        pass

    def obtain_quasi_identifier_frequencies(self, qi_list):
        for value in self.db_controller.get_frequency_of_qi_attributes(self.anonymization_table, qi_list):
            yield value