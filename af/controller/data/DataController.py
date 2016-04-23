import abc

class DataController(object):
    """Base class for all controllers that are intended to retrieve data from any type of db form

    """
    CONTROLLER_TYPE = None
    CONTROLLER_EXTENSION = None

    def __init__(self, data_location):
        self.data_location = data_location
        self.controller_type = self.CONTROLLER_TYPE

    @abc.abstractmethod
    def db_available_tables(self):
        """Returns all the available tables of a database.
        Abstract method. Not Implemented

        :rtype: list

        """
        return

    @abc.abstractmethod
    def table_columns_info(self, table_name):
        """Returns all the header data of a given table
        Abstract method. Not Implemented

        :param string table_name: name of the table which is queried
        :rtype: list

        """
        return

    @abc.abstractmethod
    def get_table_data(self, table_name):
        """Returns all the data of a given table
        Abstract method. Not Implemented

        :param string table_name: name of the table which is queried
        :rtype: list

        """
        return

    @abc.abstractmethod
    def get_table_columns_type(self, table_name):
        """Returns the types of all the columns of a given table
        Abstract method. Not Implemented

        :param string table_name: name of the table which is queried
        :rtype: string

        """
        return

    @abc.abstractmethod
    def amount_of_rows(self, table_name):
        """Returns the amount of rows a table contains
        Abstract method. Not Implemented

        :param string table_name: name of the table which is queried
        :rtype: int

        """
        return

    @abc.abstractmethod
    def get_frequency_of_qi_attributes(self, table_name, qi_list):
        """Returns the frequency of certain attributes
        Abstract method. Not Implemented

        :param string table_name: name of the table which is queried
        :param list qi_list: list of attributes to query their frequency
        :rtype: list

        """
        return

    @abc.abstractmethod
    def get_distinct_qi_values(self, table_name, qi):
        """Returns all the distinct values of a certain qi attribute

        :param string table_name: name of the table which is queried
        :param string qi: Quasi Identifier attribute name
        :rtype: list<generator>

        """
        return
