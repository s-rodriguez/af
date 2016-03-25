import os
import unittest

from af import af_directory
from af.controller.data.SqliteController import SqliteController

class TestSqliteControllerSicknessDb(unittest.TestCase):

    def setUp(self):
        db_location = os.path.join(af_directory(), 'utils', 'sickness.db')
        self.controller = SqliteController(db_location)
        self.copy_controller = SqliteController(self.create_db_copy('sickness_copy.db'))

    def tearDown(self):
        os.remove(self.copy_controller.data_location)

    def test_get_count_of_distinct_qi_values_ok(self):
        qi_key_amount = (
            ('Race', 2),
            ('Birth', 12),
            ('Gender', 2),
            ('Zip', 3),
            ('Problem', 9),
        )
        for val in qi_key_amount:
            qi, count = val
            self.assertEqual(count, list(self.controller.get_count_of_distinct_qi_values('sickness', qi))[0])

    def test_get_frequency_of_qi_attributes_ok(self):
        # 6 black and 6 white
        for result in self.controller.get_frequency_of_qi_attributes('sickness', ['Race']):
            self.assertEqual(6, result[0])

        # sickness.db is not k=2 anonymized
        qi_list = ['Race', 'Birth', 'Gender', 'Zip']
        for result in self.controller.get_frequency_of_qi_attributes('sickness', qi_list):
            self.assertGreaterEqual(2, result[0])

    def test_replace_qi_value_ok(self):
        self.assertEqual(6, self.copy_controller.get_count_of_qi_value('sickness', ['Race'], ['white']))
        self.assertEqual(0, self.copy_controller.get_count_of_qi_value('sickness', ['Race'], ['w']))
        self.copy_controller.update_qi_value('sickness', 'Race', 'w', 'white')
        self.assertEqual(0, self.copy_controller.get_count_of_qi_value('sickness', ['Race'], ['white']))
        self.assertEqual(6, self.copy_controller.get_count_of_qi_value('sickness', ['Race'], ['w']))
        self.copy_controller.update_qi_value('sickness', 'Race', 'white', 'w')
        self.assertEqual(6, self.copy_controller.get_count_of_qi_value('sickness', ['Race'], ['white']))
        self.assertEqual(0, self.copy_controller.get_count_of_qi_value('sickness', ['Race'], ['w']))

    def test_remove_row_ok(self):
        self.assertEqual(6, self.copy_controller.get_count_of_qi_value('sickness', ['Race'], ['white']))
        self.copy_controller.remove_row('sickness', ['Race'], ['white'])
        self.assertEqual(0, self.copy_controller.get_count_of_qi_value('sickness', ['Race'], ['white']))

        self.assertEqual(2, self.copy_controller.get_count_of_qi_value('sickness', ['Race', 'Gender'], ['black', 'male']))
        self.copy_controller.remove_row('sickness', ['Race', 'Gender'], ['black', 'male'])
        self.assertEqual(0, self.copy_controller.get_count_of_qi_value('sickness', ['Race', 'Gender'], ['black', 'male']))

    def test_remove_row_invalid_length_of_values(self):
        failed = False
        try:
            self.assertEqual(6, self.copy_controller.get_count_of_qi_value('sickness', ['Race'], ['white']))
            self.copy_controller.remove_row('sickness', ['Race'], ['white', ['male']])
        except Exception:
            failed = True
        self.assertTrue(failed, "Method should have failed")

    def create_db_copy(self, db_name):
        new_db_location = os.path.join(af_directory(), 'utils', db_name)
        self.controller.create_db_copy(self.controller.data_location, new_db_location)
        return new_db_location



