from af.model.algorithms.BaseAlgorithm import BaseAlgorithm
from af.utils import (
    timeit_decorator
)

class BaseKAlgorithm(BaseAlgorithm):

    def __init__(self, data_config, k):
        BaseAlgorithm.__init__(self, data_config)
        self.k = k

    def validate_arguments(self, k):
        if k < 1:
            raise Exception("Invalid k param")

    @timeit_decorator
    def validate_anonymize_conditions(self):
        print "[+] Validating anonymize conditions k = {0}...".format(str(self.k))

        counter = 0
        rows_to_remove = []
        quasi_identifier_frequencies = self.obtain_quasi_identifier_frequencies()

        for row in quasi_identifier_frequencies:
            if row[0] < self.k:
                counter += 1
                if counter > self.k:
                    print "[+] K condition not accomplished "
                    return False
                else:
                    #remove first item (the count) and add row to the list of rows to remove
                    row_item = list(row)
                    row_item.pop(0)
                    rows_to_remove.append(row_item)
        print "[+] K condition accomplished with {0} rows to remove".format(str(len(rows_to_remove)))
        self.remove_rows(rows_to_remove)
        return True

