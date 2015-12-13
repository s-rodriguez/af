

class DataController:

    def __init__(self, data_location):
        self.data_location = data_location
        self.controller_type = None

    def execute_query(self, query):
        return NotImplementedError

    def db_available_tables(self):
        return NotImplementedError

    def table_columns_info(self, table_name):
        return NotImplementedError

    def get_table_data(self, table_name):
        return NotImplementedError
