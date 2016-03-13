import os
import unittest

from af import af_directory
from af.controller.data.SqliteController import SqliteController

class TestSqliteControllerSicknessDb(unittest.TestCase):

    def setUp(self):
        db_location = os.path.join(af_directory(), 'utils', 'sickness.db')
        self.controller = SqliteController(db_location)

    def test_get_count_of_distinct_qi_values_ok(self):
        self.assertEqual(2, self.controller.get_count_of_distinct_qi_values('sickness', 'Race'))
        self.assertEqual(12, self.controller.get_count_of_distinct_qi_values('sickness', 'Birth'))
        self.assertEqual(2, self.controller.get_count_of_distinct_qi_values('sickness', 'Gender'))
        self.assertEqual(3, self.controller.get_count_of_distinct_qi_values('sickness', 'Zip'))
        self.assertEqual(9, self.controller.get_count_of_distinct_qi_values('sickness', 'Problem'))

    def test_get_frequency_of_qi_attributes_ok(self):
        query_result = self.controller.get_frequency_of_qi_attributes('sickness', ['Race'])
        # 6 black and 6 white
        for result in query_result:
            self.assertEqual(6, result)

        # sickness.db is not k=2 anonymized
        qi_list = ['Race', 'Birth', 'Gender', 'Zip']
        query_result = self.controller.get_frequency_of_qi_attributes('sickness', qi_list)
        for result in query_result:
            self.assertGreaterEqual(2, result)




