import os
import shutil
import sqlite3

from af.controller.data.DataController import DataController


class SqliteController(DataController):
    """Class that implements a way to connecting to sqlite dbs

    """
    CONTROLLER_TYPE = 'sqlite'
    CONTROLLER_EXTENSION = 'SQLite (*.sqlite3 *.db *.sqlite)'

    def __init__(self, data_location):
        DataController.__init__(self, data_location)

    def execute_query(self, query):
        """Executes a query against a loaded db table.
        Returns the query result in the form of a generator.

        :param string query: query to execute
        :rtype: list<generator>

        """
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()

            cursor.execute(query)
            for row in cursor:
                yield row

    def db_available_tables(self):
        """Returns all the available tables of a sqlite database.

        :rtype: list

        """
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = list(self.execute_query(query))
        return tables

    def table_columns_info(self, table_name):
        """Returns all the header data of a given sqlite table

        :param string table_name: name of the table which is queried
        :rtype: list

        """
        query = "SELECT * FROM {table}".format(table=table_name)
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()

            cursor.execute(query)
            columns_info = list(map(lambda x: x[0], cursor.description))
            return columns_info

    def get_table_data(self, table_name):
        """Returns all the data of a given sqlite table

        :param string table_name: name of the table which is queried
        :rtype: list

        """
        query = "SELECT * FROM {table}".format(table=table_name)
        return list(self.execute_query(query))

    def get_table_columns_type(self, table_name):
        """Returns the types of all the columns of a given sqlite table

        :param string table_name: name of the table which is queried
        :rtype: string

        """
        query = "SELECT * FROM {table} LIMIT 1".format(table=table_name)
        return [type(column) for column in list(self.execute_query(query))[0]]

    def amount_of_rows(self, table_name):
        """Returns the amount of rows a table contains

        :param string table_name: name of the table which is queried
        :rtype: int

        """
        query = "SELECT COUNT(*) FROM {table}".format(table=table_name)
        return list(self.execute_query(query))[0][0]

    def get_frequency_of_qi_attributes(self, table_name, qi_list):
        """Returns the frequency of certain attributes list on a given sqlite table.

        :param string table_name: name of the table which is queried
        :param list qi_list: list of attributes to query their frequency
        :rtype: list<generator>

        """
        query = "SELECT COUNT(*), "
        query += ','.join(qi_list) + ' '
        query += "FROM {table} GROUP BY ".format(table=table_name)
        query += ','.join(qi_list)
        for freq in self.execute_query(query):
            yield freq

    def get_frequency_of_eq_classes(self, table_name, qi_list):
        """Returns the frequency of the equivalence classes of attributes list on a given sqlite table.

        :param string table_name: name of the table which is queried
        :param list qi_list: list of attributes to query their frequency
        :rtype: list

        """
        query = "SELECT COUNT(*) FROM {table} GROUP BY ".format(table=table_name)
        query += ','.join(qi_list)
        return len(list(self.execute_query(query)))

    def get_count_of_distinct_qi_values(self, table_name, qi):
        """Returns count of distinct values of a certain qi attribute

        :param string table_name: name of the table which is queried
        :param string qi: Quasi Identifier attribute name
        :rtype: int

        """
        query = "SELECT COUNT(distinct {qi}) FROM {table}".format(table=table_name, qi=qi)
        for row in self.execute_query(query):
            yield row[0]

    def get_distinct_qi_values(self, table_name, qi):
        """Returns all the distinct values of a certain qi attribute

        :param string table_name: name of the table which is queried
        :param string qi: Quasi Identifier attribute name
        :rtype: list<generator>

        """
        query = "SELECT distinct {qi} FROM {table}".format(table=table_name, qi=qi)
        for row in self.execute_query(query):
            yield row[0]

    @staticmethod
    def create_db_copy(from_location, to_location):
        """Creates the copy of a certain db to a new location

        :param string from_location: original location of the db
        :param string to_location: new location for the db

        """
        if os.path.isfile(to_location):
            os.remove(to_location)
        shutil.copy2(from_location, to_location)

    def update_qi_value(self, table_name, qi, new_value, old_value):
        """Given a table and a qi attribute of it, it updates it's value to a new one.

        :param string table_name: name of the table which is queried
        :param string qi: Quasi Identifier attribute name
        :param string new_value: New value for the qi attribute
        :param string old_value: Current value of the qi attribute

        """
        query = "UPDATE {table} SET {qi}=? WHERE {qi}= ?".format(table=table_name, qi=qi)
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (new_value, old_value))
            conn.commit()

    def update_qi_values_in_range(self, cursor, table_name, qi, new_value, old_values):
        """Given a table and a qi attribute of it, it updates it's value to a new one for those belonging to a certain range.

        :param string table_name: name of the table which is queried
        :param string qi: Quasi Identifier attribute name
        :param string new_value: New value for the qi attribute
        :param list old_values: List of possible current values of the qi attribute

        """
        query = "UPDATE {table} SET {qi}=? WHERE {qi} IN ( ".format(table=table_name, qi=qi)
        for value in old_values:
            query += '?'
            if value != old_values[-1]:
                query += ', '
        query += ')'
        old_values.insert(0, new_value)
        cursor.execute(query, tuple(old_values))

    def update_qi_values(self, table_name, qi, dic):
        """Given a table and a qi attribute of it, it updates the qi using the dic key-value store where the key is the new value and the value of the dic are the old values

        :param string table_name: name of the table which is queried
        :param string qi: Quasi Identifier attribute name
        :param dict dicc: Dictionary containing all the updates of the form {new_value: list_of_old_values}

        """
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            for new_value, old_values in dic.iteritems():
                self.update_qi_values_in_range(cursor, table_name, qi, new_value, old_values)

    def get_count_of_qi_value(self, table_name, qi_list, values):
        """Return the amount of times a certain row contains the values of a qi attribute list

        :param string table_name: name of the table which is queried
        :param list qi_list: List containing all the qi attributes names to query
        :param list values: List of all the particular values for each of the attributes contained on the qi_list

        :rtype: int
        """
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
        """Deletes those rows on the table that match the values conditions for the qi_list attributes

        :param string table_name: name of the table which is queried
        :param list qi_list: List containing all the qi attributes names to query
        :param list values: List of all the particular values for each of the attributes contained on the qi_list

        """
        self.validate_param_lengths(qi_list, values)
        query = "DELETE FROM {table} WHERE ".format(table=table_name)
        for qi in qi_list:
            query += "{qi} = ?".format(qi=qi)
            if qi != qi_list[-1]:
                query += ' AND '
        cursor.execute(query, tuple(values))

    def remove_rows(self, table_name, qi_list, rows_to_remove):
        """Given a list of row values to remove, it deletes each one of them from the given table.

        :param string table_name: name of the table which is queried
        :param list qi_list: List containing all the qi attributes names to query
        :param list rows_to_remove: Contains all the values to remove from the table.

        """
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            for row in rows_to_remove:
                self.remove_row(cursor, table_name, qi_list, row)

    def rename_table(self, old_table_name, new_table_name):
        """Renames a certain table to a new table name

        :param string old_table_name: Current name of the table
        :param string new_table_name: New name for the table

        """
        query = "ALTER TABLE {old_table_name} RENAME TO {new_table_name}".format(old_table_name=old_table_name, new_table_name=new_table_name)
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    @staticmethod
    def validate_param_lengths(qi_list, values):
        """Validates that the qi_list attributes names coincide in length with the values associated.

        :param list qi_list: Attributes names
        :param list values: Values for the attributes of the qi_list

        """
        if len(qi_list) != len(values):
            raise Exception("The lenght of the attributes is different from the values")

    def execute_many(self, query, values_list):
        """Execute a query in the form of a typical executemany sqlite fashion

        :param string query: Query to execute in bulk mode
        :param list values_list: Values that will go taking place during the bulk query
        """
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            cursor.executemany(query, values_list)
            conn.commit()

    def get_groups_examples(self, table, qi_list):
        """Given a table name and a qi list, retrieves certain distinct rows in the form of a dictionary containing the columns info and the data sample.

        :param string table: Table name to query
        :param list qi_list: Quasi-Identifiable attributes names to group by
        :rtype: dict
        """
        query = "SELECT count(*) as amount, * from {0} GROUP BY {1} LIMIT 10;".format(table, ','.join(qi_list))
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            columns_info = list(map(lambda x: x[0].title(), cursor.description))
            data = cursor.fetchall()
            return {'columns': columns_info, 'data': data}
