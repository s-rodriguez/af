import json
import unittest

from af.model.Attribute import Attribute
from af.model.hierarchies.BaseHierarchy import BaseHierarchy
from af.model.TransformationTechnique import TransformationTechnique

class TestAttribute(unittest.TestCase):

    def setUp(self):
        self.name = 'asd'
        self.basic_type = 'string'
        self.privacy_type = None
        self.transformation_technique = None

        self.attribute = Attribute(self.name, self.basic_type, self.privacy_type, self.transformation_technique)

    def test_attribute_creation_ok(self):
        self.assertEqual(self.name, self.attribute.name, "Property not matching expected value")
        self.assertEqual(self.basic_type, self.attribute.basic_type, "Property not matching expected value")
        self.assertEqual(self.privacy_type, self.attribute.privacy_type, "Property not matching expected value")
        self.assertEqual(self.transformation_technique, self.attribute.transformation_technique, "Property not matching expected value")

    def test_representation(self):
        expected = {
            'name': self.name,
            'basic_type': self.basic_type,
            'privacy_type': self.privacy_type,
            'transformation_technique': self.transformation_technique
        }

        result = self.attribute.get_representation()

        self.assertEqual(expected, result, "Attribute representation different from expected")

    def test_load_attribute(self):
        name = 'QWER'
        basic_type = 'int'
        privacy_type = 1
        transformation_technique = None

        config = {
            'name': name,
            'basic_type': basic_type,
            'privacy_type': privacy_type,
            'transformation_technique': transformation_technique
        }

        self.attribute.load_config(config)

        self.assertEqual(name, self.attribute.name, "Property not matching expected value")
        self.assertEqual(basic_type, self.attribute.basic_type, "Property not matching expected value")
        self.assertEqual(privacy_type, self.attribute.privacy_type, "Property not matching expected value")
        self.assertEqual(transformation_technique, self.attribute.transformation_technique, "Property not matching expected value")

    def test_set_transformation_technique_ok(self):
        technique_config = {
            'name': 'SUPRESSION',
            'hierarchy': '*'*10,
        }

        self.attribute.set_transformation_technique(technique_config)

        self.assertEqual(technique_config['name'], self.attribute.transformation_technique.name, 'Property not matching expected value')
        self.assertEqual(technique_config['hierarchy'], self.attribute.transformation_technique.hierarchy.root_node.value, 'Property not matching expected value')


    def test_get_transformation_technique_representation(self):
        technique_config = {
            'name': 'SUPRESSION',
            'hierarchy': '*'*10,
        }

        self.attribute.set_transformation_technique(technique_config)
        result = self.attribute.get_transformation_technique_representation()

        self.assertEqual(technique_config, result)