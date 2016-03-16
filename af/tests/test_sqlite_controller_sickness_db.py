import os
import unittest

from af import af_directory
from af.controller.data.SqliteController import SqliteController

class TestSqliteControllerSicknessDb(unittest.TestCase):

    def setUp(self):
        db_location = os.path.join(af_directory(), 'utils', 'sickness.db')
        self.controller = SqliteController(db_location)

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
            self.assertEqual(6, result)

        # sickness.db is not k=2 anonymized
        qi_list = ['Race', 'Birth', 'Gender', 'Zip']
        for result in self.controller.get_frequency_of_qi_attributes('sickness', qi_list):
            self.assertGreaterEqual(2, result)
