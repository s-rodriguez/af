import logging

from af.model.algorithms.BaseKAlgorithm import BaseKAlgorithm
from af.utils import (
    K_PRIVACY_MODEL,
    ANONYMIZED_DATA_TABLE,
)


class Datafly(BaseKAlgorithm):
    """Datafly Algorithm implementation

    """
    PRIVACY_MODEL = K_PRIVACY_MODEL
    ALGORITHM_NAME = 'Datafly'

    def __init__(self, data_config, k, optimized_processing=False):
        BaseKAlgorithm.__init__(self, data_config, k, optimized_processing)
        self.logger = logging.getLogger('algorithms.Datafly')
        self.iteration = 0

    def process(self):
        """The main core algorithm to anonymize using the Datafly implementation

        """
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

    def on_post_process(self):
        """After anonymizing, rename table to the common Anonymization Table Name defined.

        """
        self.anon_db_controller.rename_table(self.anonymization_table, ANONYMIZED_DATA_TABLE)
        self.anonymization_table = ANONYMIZED_DATA_TABLE



