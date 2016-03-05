import csv

from af.controller.data.DataController import DataController


class CSVController(DataController):

    CONTROLLER_TYPE = 'csv'
    CONTROLLER_EXTENSION = 'CSV (*.csv)'

    def __init__(self, data_location):
        DataController.__init__(self, data_location)
        self.rows = None

    def db_available_tables(self):
        return [[self._file_name()]]

    def table_columns_info(self, table_name=None):
        if self.rows is None:
            self._load_csv()
        return self.rows[0]

    def get_table_data(self, table_name=None):
        if self.rows is None:
            self._load_csv()
        return self.rows[1:]

    def _file_name(self):
        return self.data_location.split('/')[-1]

    def _load_csv(self):
        with open(self.data_location, 'rb') as csv_file:
            reader = csv.reader(csv_file)
            self.rows = [row for row in reader]

    def get_table_columns_type(self, table_name=None):
        if self.rows is None:
            self._load_csv()
        amount_of_columns = len(self.rows[0])
        return [type('') for i in range(0, amount_of_columns)]

    def amount_of_rows(self, table_name=None):
        if self.rows is None:
            self._load_csv()
        return len(self.rows)-1
