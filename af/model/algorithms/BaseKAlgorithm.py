import logging

from af.model.algorithms.BaseAlgorithm import BaseAlgorithm
from af.utils import (
    timeit_decorator
)


class BaseKAlgorithm(BaseAlgorithm):
    """Class extending from the BaseAlgorithm class. It is intended to be a model for those algoritm implementations that have the k-anonymization as a model.

    """
    def __init__(self, data_config, k, optimized_processing=False):
        BaseAlgorithm.__init__(self, data_config, optimized_processing)
        self.k = k
        self.logger = logging.getLogger('algorithms.BaseKAlgorithm')

    def validate_arguments(self):
        """Validates all the arguments that are used during the anonymization process. If an error occurs, it throws an exception

        :rtype: True if arguments are valid.

        """
        BaseAlgorithm.validate_arguments(self)
        try:
            self.k = int(self.k)
        except:
            error_message = "K param must be an int"
            self.logger.error(error_message)
            raise Exception(error_message)

        if self.k < 1:
            error_message = "Invalid k param"
            self.logger.error(error_message)
            raise Exception(error_message)

        return True

    @timeit_decorator
    def validate_anonymize_conditions(self):
        """Validates the K anonymization condition

        :rtype: Boolean indicating if condition has been met or not.

        """
        self.logger.info("Validating anonymize conditions k = {0}...".format(str(self.k)))

        counter = 0
        rows_to_remove = []
        quasi_identifier_frequencies = self.obtain_quasi_identifier_frequencies()

        for row in quasi_identifier_frequencies:
            if row[0] < self.k:
                counter += 1
                if counter > self.k:
                    self.logger.info("K condition not accomplished ")
                    return False
                else:
                    #remove first item (the count) and add row to the list of rows to remove
                    row_item = list(row)
                    row_item.pop(0)
                    rows_to_remove.append(row_item)
        self.logger.info("K condition accomplished with {0} rows to remove".format(str(len(rows_to_remove))))
        self.remove_rows(rows_to_remove)
        return True
