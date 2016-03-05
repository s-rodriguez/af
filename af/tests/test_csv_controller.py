import os
import unittest

from af import af_directory
from af.controller.data.CSVController import CSVController

class TestCSVController(unittest.TestCase):

    def setUp(self):
        db_location = os.path.join(af_directory(), 'utils', 'test.csv')
        self.controller = CSVController(db_location)


    def test_available_tables_ok(self):
        tables_expected = [['test.csv']]

        tables_result = self.controller.db_available_tables()

        self.assertEqual(tables_expected, tables_result, "The tables do not match")

    def test_table_columns_info_ok(self):
        expected_info = ['Id', 'Name', 'Price']

        columns_info = self.controller.table_columns_info('Cars')
        print columns_info
        self.assertTrue(len(columns_info) == 3, "There should be data retrieved")
        self.assertEqual(expected_info, columns_info, "Data retrieved do not match with expected")

    def test_get_table_data_ok(self):
        first_record = ['1', 'Audi', '52642']

        data_result = self.controller.get_table_data('Cars')

        self.assertTrue(len(data_result) == 8, "There should be data retrieved")
        self.assertEqual(first_record, data_result[0], "Data retrieved do not match with expected")

    def test_get_table_column_type_ok(self):
        column_types = self.controller.get_table_columns_type('Cars')

        self.assertTrue(len(column_types) == 3, "There should be data retrieved")
        self.assertEqual(str, column_types[0], "First column should be int type")

    def test_amount_of_rows_ok(self):
        row_count = self.controller.amount_of_rows('Cars')

        self.assertTrue(row_count == 8, "There should be 8 rows in the table")

