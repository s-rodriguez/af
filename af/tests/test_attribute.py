import json
import unittest

from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController
from af.model.Attribute import Attribute
from af.model.hierarchies.BaseHierarchy import BaseHierarchy


class TestAttribute(unittest.TestCase):

    def setUp(self):
        self.name = 'asd'
        self.basic_type = int
        self.privacy_type = None
        self.weight = 0
        self.hierarchy_none = None

        self.attribute = Attribute(self.name, self.basic_type, self.privacy_type, self.hierarchy_none, self.weight)

        self.saved_hierarchy = {BaseHierarchy.supression_node().value: {1: {2: {3: None}}}}
        self.hierarchy = BaseHierarchyController().load_hierarchy(self.saved_hierarchy, attribute_type=int)

    def test_attribute_creation_ok(self):
        self.assertEqual(self.name, self.attribute.name, "Property not matching expected value")
        self.assertEqual(self.basic_type, self.attribute.basic_type, "Property not matching expected value")
        self.assertEqual(self.privacy_type, self.attribute.privacy_type, "Property not matching expected value")
        self.assertEqual(self.hierarchy_none, self.attribute.hierarchy, "Property not matching expected value")
        self.assertEqual(self.weight, self.attribute.weight, "Property not matching expected value")

    def test_representation(self):
        expected = {
            'name': self.name,
            'basic_type': self.basic_type,
            'privacy_type': self.privacy_type,
            'weight': self.weight,
            'hierarchy': self.hierarchy_none
        }

        result = self.attribute.get_representation()

        self.assertEqual(expected, result, "Attribute representation different from expected")

    def test_load_attribute(self):
        name = 'QWER'
        basic_type = 'int'
        privacy_type = 1
        hierarchy = None
        weight = 0

        config = {
            'name': name,
            'basic_type': basic_type,
            'privacy_type': privacy_type,
            'weight': weight,
            'hierarchy': hierarchy
        }

        self.attribute.load_config(config)

        self.assertEqual(name, self.attribute.name, "Property not matching expected value")
        self.assertEqual(basic_type, self.attribute.basic_type, "Property not matching expected value")
        self.assertEqual(privacy_type, self.attribute.privacy_type, "Property not matching expected value")
        self.assertEqual(hierarchy, self.attribute.hierarchy, "Property not matching expected value")
        self.assertEqual(weight, self.attribute.weight, "Property not matching expected value")

    def test_set_hierarchy_ok(self):
        self.attribute.set_hierarchy(self.saved_hierarchy)

        self.assertEqual(BaseHierarchy.supression_node().value, self.attribute.hierarchy.root_node.value, 'Property not matching expected value')
        self.assertTrue(len(self.attribute.hierarchy.leaf_nodes)==1, 'Property not matching expected value')

    def test_get_hierarchy_representation(self):
        self.attribute.set_hierarchy(self.saved_hierarchy)
        result = self.attribute.get_hierarchy_representation()

        self.assertEqual(self.saved_hierarchy, result)

    def test_transform_ok(self):
        self.attribute.hierarchy = self.hierarchy

        result0 = self.attribute.transform(3, 0)
        result1 = self.attribute.transform(3, 1)
        result2 = self.attribute.transform(3, 2)
        result3 = self.attribute.transform(3, 3)

        self.assertEqual(3, result0, "Transformation gave an unexpected result")
        self.assertEqual(2, result1, "Transformation gave an unexpected result")
        self.assertEqual(1, result2, "Transformation gave an unexpected result")
        self.assertEqual(BaseHierarchy.supression_node().value, result3, "Transformation gave an unexpected result")

    def test_trasnform_raises_exception(self):
        failed = False
        try:
            self.attribute.transform(1, 3)
        except Exception:
            failed = True

        self.assertTrue(failed, "Transformation should have failed with no hierarchy")
