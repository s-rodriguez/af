import json
import os
import unittest

from af.exceptions import ImportException
from af.model.Attribute import Attribute
from af.model.DataConfig import DataConfig
import af.utils as utils

class TestDataConfig(unittest.TestCase):

    def test_data_config_creation_ok(self):
        project = None

        dc = DataConfig(project)

        self.assertEqual(None, dc.project, "Property not matching expected value")
        self.assertEqual(None, dc.location, "Property not matching expected value")
        self.assertEqual(None, dc.type, "Property not matching expected value")
        self.assertEqual(None, dc.table, "Property not matching expected value")
        self.assertEqual([], dc.attributes_list, "Property not matching expected value")

    def test_config_representation(self):
        project = None
        dc = DataConfig(project)

        expected = json.dumps({
            'location': None,
            'data_type': None,
            'table': None,
            'attributes': [],
        })

        result = dc.config_representation()

        self.assertEqual(expected, result, "Representation doesnt match with expected one")


    def test_load_config(self):
        mock_location = os.path.abspath(__file__)
        json_config = json.dumps({
            'location': mock_location,
            'data_type': None,
            'table': None,
            'attributes': [{'name': 'xxx'}],
        })

        dc = DataConfig(None)
        dc.load_config(json_config)

        self.assertEqual(mock_location, dc.location, "Different location than expected")
        self.assertEqual(None, dc.type, "Different type than expected")
        self.assertEqual(None, dc.table, "Different table than expected")
        self.assertTrue(len(dc.attributes_list) == 1, "There should be one attribute added")
        self.assertEqual('xxx', dc.attributes_list[0].name, "Attribute name different from expected")


    def test_validate_config_to_load(self):
        config = {
            'location': 'asdffdsa',
            'data_type': None,
            'table': None,
            'attributes': [],
        }
        dc = DataConfig(None)

        failed = False
        try:
            dc.validate_config_to_load(config)
        except ImportException:
            failed = True

        self.assertTrue(failed, "Method validating should fail")

    def test_retrieve_qi_or_identifiable_attributes_ok(self):
        attributes = [
                        Attribute('Identifiable', privacy_type=utils.PRIVACY_TYPE_IDENTIFIER),
                        Attribute('Quasi-Identifier 1', privacy_type=utils.PRIVACY_TYPE_QI),
                        Attribute('Quasi-Identifier 2', privacy_type=utils.PRIVACY_TYPE_QI),
        ]

        dc = DataConfig(None, attributes_list=attributes)

        result_identifiable = dc.get_privacy_type_attributes_list(utils.PRIVACY_TYPE_IDENTIFIER)
        result_qi = dc.get_privacy_type_attributes_list(utils.PRIVACY_TYPE_QI)

        self.assertTrue(len(result_identifiable) == 1, "The list of identifiables should have one element")
        self.assertEqual(attributes[0], result_identifiable[0], "Retrieved an unexpected Identifiable attribute")

        self.assertTrue(len(result_qi) == 2, "The list of identifiables should have two elements")
        for i in range(1,3):
            self.assertTrue(attributes[i] in result_qi, "A qi was not retrieved correctly")
