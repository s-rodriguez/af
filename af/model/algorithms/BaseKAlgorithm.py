from af.model.algorithms.BaseAlgorithm import BaseAlgorithm
class BaseKAlgorithm(BaseAlgorithm):

    def __init__(self, data_config, k):
        BaseAlgorithm.__init__(self, data_config)
        if k < 1:
            raise Exception("Invalid k param")
        self.k = k

    def validate_anonymize_conditions(self):
        counter = 0
        rows_to_remove = []
        quasi_identifier_frequencies = self.db_controller.obtain_quasi_identifier_frequencies(self.anonymization_table, self.qi_attributes)

        for row in quasi_identifier_frequencies:
            if row[0] < self.k:
                counter += 1
                if counter > self.k:
                    return False
                else:
                    #remove first item (the count) andd add row to the list of rows to remove
                    row.pop(1)
                    rows_to_remove.append(row)

        self.remove_rows(rows_to_remove)
        return True

