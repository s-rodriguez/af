import csv

from af.controller.data.DataController import DataController


class CSVController(DataController):

    def __init__(self, data_location):
        DataController.__init__(self, data_location)
        self.controller_type = 'csv'
        self.rows = None

    def db_available_tables(self):
        return self._file_name()

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

if __name__ == '__main__':
    location = '/home/srodriguez/repos/edat/edat/utils/test.csv'
    csv_controller = CSVController(location)
    print csv_controller.db_available_tables()
    print csv_controller.table_columns_info()
    print csv_controller.get_table_data()
