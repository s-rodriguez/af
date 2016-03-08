import abc

class DataController(object):

    CONTROLLER_TYPE = None
    CONTROLLER_EXTENSION = None

    def __init__(self, data_location):
        self.data_location = data_location
        self.controller_type = self.CONTROLLER_TYPE

    @abc.abstractmethod
    def db_available_tables(self):
        return

    @abc.abstractmethod
    def table_columns_info(self, table_name):
        return

    @abc.abstractmethod
    def get_table_data(self, table_name):
        return

    @abc.abstractmethod
    def get_table_columns_type(self, table_name):
        return

    @abc.abstractmethod
    def amount_of_rows(self, table_name):
        return

    @abc.abstractmethod
    def get_frequency_of_qi_attributes(self, table_name, qi_list):
        return
