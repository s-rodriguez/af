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
        query = "SELECT COUNT(*), "
        query += ','.join(qi_list) + ' '
        query += "FROM {table} GROUP BY ".format(table=table_name)
        query += ','.join(qi_list)
        for freq in self.execute_query(query):
            yield freq

    def get_frequency_of_eq_classes(self, table_name, qi_list):
        query = "SELECT COUNT(*) FROM {table} GROUP BY ".format(table=table_name)
        query += ','.join(qi_list)
        return len(list(self.execute_query(query)))

    def get_count_of_distinct_qi_values(self, table_name, qi):
        query = "SELECT COUNT(distinct {qi}) FROM {table}".format(table=table_name, qi=qi)
        for row in self.execute_query(query):
            yield row[0]

    def get_distinct_qi_values(self, table_name, qi):
        query = "SELECT distinct {qi} FROM {table}".format(table=table_name, qi=qi)
        for row in self.execute_query(query):
            yield row[0]

    @staticmethod
    def create_db_copy(from_location, to_location):
        if os.path.isfile(to_location):
            os.remove(to_location)
        shutil.copy2(from_location, to_location)

    def update_qi_value(self, table_name, qi, new_value, old_value):
        query = "UPDATE {table} SET {qi}=? WHERE {qi}= ?".format(table=table_name, qi=qi)
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (new_value, old_value))
            conn.commit()

    def update_qi_values_in_range(self, cursor, table_name, qi, new_value, old_values):
        query = "UPDATE {table} SET {qi}=? WHERE {qi} IN ( ".format(table=table_name, qi=qi)
        for value in old_values:
            query += '?'
            if value != old_values[-1]:
                query += ', '
        query += ')'
        old_values.insert(0, new_value)
        cursor.execute(query, tuple(old_values))

    def update_qi_values(self, table_name, qi, dic):
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            for new_value, old_values in dic.iteritems():
                self.update_qi_values_in_range(cursor, table_name, qi, new_value, old_values)

    def get_count_of_qi_value(self, table_name, qi_list, values):
        self.validate_param_lengths(qi_list, values)
        query = "SELECT COUNT(*) FROM {table} WHERE ".format(table=table_name)
        for qi in qi_list:
            query += "{qi} = ?".format(qi=qi)
            if qi != qi_list[-1]:
                query += ' AND '

        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            return list(cursor.execute(query, tuple(values)))[0][0]

    def remove_row(self, cursor, table_name, qi_list, values):
        self.validate_param_lengths(qi_list, values)
        query = "DELETE FROM {table} WHERE ".format(table=table_name)
        for qi in qi_list:
            query += "{qi} = ?".format(qi=qi)
            if qi != qi_list[-1]:
                query += ' AND '
        cursor.execute(query, tuple(values))

    def remove_rows(self, table_name, qi_list, rows_to_remove):
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            for row in rows_to_remove:
                self.remove_row(cursor, table_name, qi_list, row)

    def rename_table(self, old_table_name, new_table_name):
        query = "ALTER TABLE {old_table_name} RENAME TO {new_table_name}".format(old_table_name=old_table_name, new_table_name=new_table_name)
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    @staticmethod
    def validate_param_lengths(qi_list, values):
        if len(qi_list) != len(values):
            raise Exception("The lenght of the attributes is different from the values")

    def execute_many(self, query, values_list):
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            cursor.executemany(query, values_list)
            conn.commit()

    def get_groups_examples(self, table, qi_list):
        query = "SELECT count(*) as amount, * from {0} GROUP BY {1} LIMIT 30;".format(table, ','.join(qi_list))
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            columns_info = list(map(lambda x: x[0], cursor.description))
            data = cursor.fetchall()
            return {'columns': columns_info, 'data': data}
