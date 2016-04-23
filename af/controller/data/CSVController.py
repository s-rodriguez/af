import csv

from af.controller.data.DataController import DataController


class CSVController(DataController):
    """Class that can handles csv data files

    """
    CONTROLLER_TYPE = 'csv'
    CONTROLLER_EXTENSION = 'CSV (*.csv)'

    def __init__(self, data_location):
        DataController.__init__(self, data_location)
        self.rows = None

    def db_available_tables(self):
        """Returns the csv file name. Because it's a csv file, and not a db, the table is unique and is the one expressed on the document

        :rtype: string

        """
        return [[self._file_name()]]

    def table_columns_info(self, table_name=None):
        """Returns the the header data of a specific table. Because it is a csv file, it is assumed that the header data will be contained on the first row of the file.

        :param string table_name: name of the table which is to be loaded
        :rtype: string

        """
        if self.rows is None:
            self._load_csv()
        return self.rows[0]

    def get_table_data(self, table_name=None):
        """Returns all the data of the csv file. It avoids the first row, as it is the one assumed to have the header data.

        :param string table_name: name of the table which is to be loaded
        :rtype: list

        """
        if self.rows is None:
            self._load_csv()
        return self.rows[1:]

    def _file_name(self):
        """Returns the file name, without the directory path

        :rtype: string

        """
        return self.data_location.split('/')[-1]

    def _load_csv(self):
        """Loads the entire csv on memory for further use. Use with care, for small files.

        """
        with open(self.data_location, 'rb') as csv_file:
            reader = csv.reader(csv_file)
            self.rows = [row for row in reader]

    def get_table_columns_type(self, table_name=None):
        """Returns the types of the columns of a given table

        :param string table_name: name of the table which is to be loaded
        :rtype: list

        """
        if self.rows is None:
            self._load_csv()
        amount_of_columns = len(self.rows[0])
        return [type('') for i in range(0, amount_of_columns)]

    def amount_of_rows(self, table_name=None):
        """Returns the amount of rows the file contains.

        :param string table_name: name of the table
        :rtype: int

        """
        if self.rows is None:
            self._load_csv()
        return len(self.rows)-1

    @staticmethod
    def create_db_copy(from_location, to_location):
        return NotImplementedError

    def get_distinct_qi_values(self, table_name, qi):
        # TODO: implementar
        """Returns all the distinct values of a certain qi attribute

        :param string table_name: name of the table which is queried
        :param string qi: Quasi Identifier attribute name
        :rtype: list<generator>

        """
        return NotImplementedError
