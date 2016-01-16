import sqlite3

from af.controller.data.DataController import DataController


class SqliteController(DataController):

    def __init__(self, data_location):
        DataController.__init__(self, data_location)
        self.controller_type = 'sqlite'

    def _execute_query(self, query):
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()

            cursor.execute(query)
            for row in cursor:
                yield row

    def db_available_tables(self):
        """
        From a given sqlite db, it looks for all the tables that exist
        :return: list with all available tables
        """
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = list(self._execute_query(query))
        return tables

    def table_columns_info(self, table_name):
        query = "SELECT * FROM {table}".format(table=table_name)
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()

            cursor.execute(query)
            columns_info = list(map(lambda x: x[0], cursor.description))
            return columns_info

    def get_table_data(self, table_name):
        query = "SELECT * FROM {table}".format(table=table_name)
        return list(self._execute_query(query))

if __name__ == '__main__':
    location = '/home/srodriguez/repos/edat/edat/utils/test.db'
    sqlite_controller = SqliteController(location)
    print sqlite_controller.db_available_tables()
    print sqlite_controller.table_columns_info('Cars')
    print sqlite_controller.get_table_data('Cars')
