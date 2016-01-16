

class DataController(object):

    CONTROLLER_TYPE = None

    def __init__(self, data_location):
        self.data_location = data_location
        self.controller_type = self.CONTROLLER_TYPE

    def db_available_tables(self):
        return NotImplementedError

    def table_columns_info(self, table_name):
        return NotImplementedError

    def get_table_data(self, table_name):
        return NotImplementedError
