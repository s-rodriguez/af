import logging
import time

from af.controller.data.SqliteController import SqliteController

from af.controller.anonymization.PreProcessingStage import PreProcessingStage

from af import utils
from af.utils import (
    timeit_decorator,
    ADDITIONAL_INFO_TABLE,
)


class BaseAlgorithm(object):
    """Base class for all algorithms that are to be implemented.
    It details all the necessary methods that are going to be used to achieve a successful anonymization.
    Some are already implemented and shouldn't be changed, other were left as not implemented with the purpose fo each algorithm to design it based on its own necessities

    """
    PRIVACY_MODEL = None
    ALGORITHM_NAME = None

    def __init__(self, data_config, optimized_processing=False):
        self.data_config = data_config
        self.optimized_processing = optimized_processing

        self.id_attributes = data_config.get_privacy_type_attributes_list(utils.PRIVACY_TYPE_IDENTIFIER)

        # qi attributes ordered by weight
        self.qi_attributes = sorted(data_config.get_privacy_type_attributes_list(utils.PRIVACY_TYPE_QI),
                                    key=lambda x: x.weight,
                                    reverse=True)

        self.other_attributes = data_config.get_normal_type_attributes_list()

        self.anon_db_location = utils.get_anonymization_db_location()
        self.anon_db_controller = SqliteController(self.anon_db_location)

        self.anonymization_table = data_config.table
        self.metrics_table = ADDITIONAL_INFO_TABLE
        self.logger = logging.getLogger('algorithms.BaseAlgorithm')

        self.additional_anonymization_info = {}

    def validate_arguments(self):
        """Validates all the arguments that are used during the anonymization process

        :rtype: Boolean True/False

        """
        return self.data_config.validate_for_anonymization()

    def process(self):
        """Abstract method. Inside of it all the directives to be used to complete the anonymization process must be put.

        """
        pass

    def validate_anonymize_conditions(self):
        """Validates the anonymization conditions. Abstract Method.

        """
        pass

    def on_pre_process(self):
        """All the steps that are preconditions to be executed for the anonymization process, should be put in here.
        The method is called prior to the process method during the anonymization.
        The BaseAlgorithm class calls the minimum intended to validate the conditions: validates the arguments, and calls the PreProcessingStage preprocess method.

        """
        self.validate_arguments()
        pre_processing_stage = PreProcessingStage(self.data_config)
        pre_processing_stage.preprocess()

    def on_post_process(self):
        """All the steps that are to be taken after the transformation process, should be put in here.
        The method is called after the process method during the anonymization.

        """
        pass

    @timeit_decorator
    def obtain_quasi_identifier_frequencies(self):
        """Returns a list<generator> with all the quasi identifier attributes frequencies

        :rtype: List<generator> with a frequency count.
        """
        qi_list = [att.name for att in self.qi_attributes]
        for value in self.anon_db_controller.get_frequency_of_qi_attributes(self.anonymization_table, qi_list):
            yield value

    @timeit_decorator
    def obtain_qi_most_frequently(self):
        """Returns the quasi-identifier with the most appearances in the table to anonymize.

        :rtype: class:`af.model.Attribute` instance

        """
        self.logger.info("Obtaining qi most frequently ...")

        qi_most_frequently = None
        qi_most_frequently_count = 0
        for qi in self.qi_attributes:
            frequency = list(self.anon_db_controller.get_count_of_distinct_qi_values(self.anonymization_table, qi.name))[0]
            if (qi_most_frequently is None) or (frequency > qi_most_frequently_count) \
               or ((frequency == qi_most_frequently_count) and (qi.weight > qi_most_frequently.weight)):
                qi_most_frequently = qi
                qi_most_frequently_count = frequency

        self.logger.info("The qi most frequently is {0} with {1} occurrences ".format(str(qi_most_frequently.name), str(qi_most_frequently_count)))

        return qi_most_frequently

    @timeit_decorator
    def update_qi_values(self, qi, dic):
        """Given a quasi-identifier and a dictionary with values, it updates the qi values on the table

        :param qi: Attribute instance
        :param dict dic: Dictionary containing {new_value: old_values}

        """
        self.logger.info("Updating qi {0} , {1} values to update...".format(str(qi.name), str(len(dic))))
        self.anon_db_controller.update_qi_values(self.anonymization_table, qi.name, dic)

    @timeit_decorator
    def remove_rows(self, rows_to_remove):
        """Given a list of rows, it removes them from the table being anonymized.

        :param list rows_to_remove: Information about the rows that are to be deleted

        """
        self.logger.info("Removing {0} rows ...".format(str(len(rows_to_remove))))
        qi_list = [att.name for att in self.qi_attributes]
        self.anon_db_controller.remove_rows(self.anonymization_table, qi_list, rows_to_remove)

    @timeit_decorator
    def insert_additional_information(self):
        """During the anonymization process, all the algorithms can leave additional information about what happenned during the transformation.
        The information is first stored on a dictionary. This dictionary is then to be dumped on a specific table designed for this additional information.

        """
        values = []
        for k in sorted(self.additional_anonymization_info):
            v = self.additional_anonymization_info[k]
            values.append((str(v[0]), str(v[1])))
        query = "INSERT INTO {0} (key, value) VALUES (?, ?);".format(self.metrics_table)
        self.anon_db_controller.execute_many(query, values)

    def save_anonymization_info_on_data_config(self):
        """After the anonymization process, the data configuration instance has to be populated with information about the new db location, the anonymized table, and the metrics table (which contains additional information about the transformation process)

        """
        self.data_config.anonymized_db_location = self.anon_db_location
        self.data_config.anonymized_table = self.anonymization_table
        self.data_config.metrics_table = self.metrics_table

    @timeit_decorator
    def anonymize(self):
        """Base method that is called every time an anonymization wants to take place.
        It calls the methods necessary to achieve the transformation.

        """
        try:
            time_start = time.time()

            self.on_pre_process()
            self.process()
            self.on_post_process()

            time_end = time.time()
            elapsed_time = time_end - time_start

            self.anonymization_duration = '%2.2f seconds' % elapsed_time
            self.additional_anonymization_info[0] = ('Algorithm Name', self.ALGORITHM_NAME)
            self.additional_anonymization_info[1] = ('Anonymization Duration', self.anonymization_duration)
            self.insert_additional_information()
            self.save_anonymization_info_on_data_config()

        except Exception, e:
            return e.message

        return None
