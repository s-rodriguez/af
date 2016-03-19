import os
import shutil
import sqlite3

from af.controller.data.DataController import DataController


class SqliteController(DataController):

    CONTROLLER_TYPE = 'sqlite'
    CONTROLLER_EXTENSION = 'SQLite (*.sqlite3 *.db *.sqlite)'

    def __init__(self, data_location):
        DataController.__init__(self, data_location)

    def execute_query(self, query):
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
        tables = list(self.execute_query(query))
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
        return list(self.execute_query(query))

    def get_table_columns_type(self, table_name):
        query = "SELECT * FROM {table} LIMIT 1".format(table=table_name)
        return [type(column) for column in list(self.execute_query(query))[0]]

    def amount_of_rows(self, table_name):
        query = "SELECT COUNT(*) FROM {table}".format(table=table_name)
        return list(self.execute_query(query))[0][0]

    def get_frequency_of_qi_attributes(self, table_name, qi_list):
        query = "SELECT COUNT(*) ".format(table=table_name)
        if len(qi_list) == 1:
            query += ', '
        query += ','.join(qi_list) + ' '
        query += "FROM {table} GROUP BY ".format(table=table_name)
        query += ','.join(qi_list)
        for freq in self.execute_query(query):
            yield freq

    def get_count_of_distinct_qi_values(self, table_name, qi):
        query = "SELECT COUNT(distinct {qi}) FROM {table}".format(table=table_name, qi=qi)
        for row in self.execute_query(query):
            yield row[0]

    @staticmethod
    def create_db_copy(from_location, to_location):
        if os.path.isfile(to_location):
            os.remove(to_location)
        shutil.copy2(from_location, to_location)

    def replace_qi_value(self, table_name, qi, new_value, old_value):
        query = "UPDATE {table} SET {qi}=? WHERE {qi}= ?".format(table=table_name, qi=qi)
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (new_value, old_value))
            conn.commit()

    def get_count_of_qi_value(self, table_name, qi_list, values):
        query = "SELECT COUNT(*) FROM {table} WHERE ".format(table=table_name)
        for qi in qi_list:
            query += "{qi} = ?".format(qi=qi)
            if qi != qi_list[-1]:
                query += ' AND '

        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            return list(cursor.execute(query, tuple(values)))[0][0]

    def remove_row(self, table_name, qi_list, values):
        query = "DELETE FROM {table} WHERE ".format(table=table_name)
        for qi in qi_list:
            query += "{qi} = ?".format(qi=qi)
            if qi != qi_list[-1]:
                query += ' AND '
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(values))
            conn.commit()

