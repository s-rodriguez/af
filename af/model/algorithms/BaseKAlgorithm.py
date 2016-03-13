from af.model.algorithms.BaseAlgorithm import BaseAlgorithm
class BaseKAlgorithm(BaseAlgorithm):

    def __init__(self, data_config, k):
        BaseAlgorithm.__init__(self, data_config)
        if k < 1:
            raise Exception("Invalid k param")
        self.k = k

    def validate_anonymize_conditions(self, qi_list):
        quasi_identifier_frequencies = self.db_controller.obtain_quasi_identifier_frequencies(self.anonymization_table, qi_list)
        for frequency in quasi_identifier_frequencies:
            if frequency < self.k:
                return False
        return True

