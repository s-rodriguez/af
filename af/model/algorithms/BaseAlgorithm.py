from af.controller.data.SqliteController import SqliteController
from af import utils
from af.controller.anonymization.PreProcessingStage import PreProcessingStage
from af.utils import (
    timeit_decorator
)

class BaseAlgorithm(object):

    def __init__(self, data_config):
        self.data_config = data_config

        self.id_attributes = data_config.get_privacy_type_attributes_list(utils.PRIVACY_TYPE_IDENTIFIER)
        self.qi_attributes = data_config.get_privacy_type_attributes_list(utils.PRIVACY_TYPE_QI)
        self.other_attributes = data_config.get_normal_type_attributes_list()

        self.anon_db_controller = SqliteController(utils.get_anonymization_db_location())

        self.anonymization_table = data_config.table

    def validate_arguments(self):
        pass

    def process(self):
        pass

    def validate_anonymize_conditions(self):
        pass

    def on_pre_process(self):
        pre_processing_stage = PreProcessingStage(self.data_config)
        pre_processing_stage.preprocess()

    def on_post_process(self):
        pass

    @timeit_decorator
    def obtain_quasi_identifier_frequencies(self):
        qi_list = [att.name for att in self.qi_attributes]
        for value in self.anon_db_controller.get_frequency_of_qi_attributes(self.anonymization_table, qi_list):
            yield value

    @timeit_decorator
    def obtain_qi_most_frequently(self):
        print "[+] Obtaining qi most frequently ..."

        qi_most_frequently = None
        qi_most_frequently_count = 0
        for qi in self.qi_attributes:
            frequency = list(self.anon_db_controller.get_count_of_distinct_qi_values(self.anonymization_table, qi.name))[0]
            if (qi_most_frequently is None) or (frequency > qi_most_frequently_count) \
               or ((frequency == qi_most_frequently_count) and (qi.weight > qi_most_frequently.weight)):
                qi_most_frequently = qi
                qi_most_frequently_count = frequency

        print "[+] The qi most frequently is {0} with {1} occurrences ".format(str(qi_most_frequently.name), str(qi_most_frequently_count))

        return qi_most_frequently

    @timeit_decorator
    def update_qi_values(self, qi, dic):
        print "[+] Updating qi {0} , {1} values to update...".format(str(qi.name), str(len(dic)))
        self.anon_db_controller.update_qi_values(self.anonymization_table, qi.name, dic)

    @timeit_decorator
    def remove_rows(self, rows_to_remove):
        print "[+] Removing {0} rows ...".format(str(len(rows_to_remove)))
        qi_list = [att.name for att in self.qi_attributes]
        self.anon_db_controller.remove_rows(self.anonymization_table, qi_list, rows_to_remove)

    @timeit_decorator
    def anonymize(self):
        self.on_pre_process()
        self.process()
        self.on_post_process()
