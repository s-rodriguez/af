import unittest

from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController
from af.model.TransformationTechnique import TransformationTechnique
from af.model.hierarchies.BaseHierarchy import BaseHierarchy


class TestTransformationTechnique(unittest.TestCase):

    def setUp(self):
        bh_controller = BaseHierarchyController(BaseHierarchy())
        saved_hierarchy = {"**********": {1: {2: 3}}}
        self.hierarchy = bh_controller.load_hierarchy(saved_hierarchy, attribute_type=int)

    def test_creation_ok(self):
        name = 'asdf'
        tt = TransformationTechnique(name, self.hierarchy)

        self.assertEqual(name, tt.name, 'Property not matching expected value')
        self.assertEqual(self.hierarchy, tt.hierarchy, 'Property not matching expected value')

    def test_transformation_ok(self):
        name = 'asdf'
        tt = TransformationTechnique(name, self.hierarchy)

        result0 = tt.transform(3, 0)
        result1 = tt.transform(3, 1)
        result2 = tt.transform(3, 2)
        result3 = tt.transform(3, 3)

        self.assertEqual(3, result0, "Transformation gave an unexpected result")
        self.assertEqual(2, result1, "Transformation gave an unexpected result")
        self.assertEqual(1, result2, "Transformation gave an unexpected result")
        self.assertEqual('*'*10, result3, "Transformation gave an unexpected result")

    def test_trasnformation_raises_exception(self):
        tt = TransformationTechnique('asdf', None)

        failed = False
        try:
            tt.transform(1, 3)
        except Exception:
            failed = True

        self.assertTrue(failed, "Transformation should have failed with no hierarchy")

    def test_get_representation_ok(self):
        name = 'asdf'
        tt = TransformationTechnique(name, self.hierarchy)

        expected = {
            'name': name,
            'hierarchy': self.hierarchy.hierarchy_representation()
        }

        result = tt.get_representation()

        self.assertEqual(expected, result, "Unexpected representation")


    def test_load_technique_ok(self):
        config = {
            'name': 'asdf',
            'hierarchy': '*'*10,
        }
        h = BaseHierarchy()
        tt = TransformationTechnique.load_technique(config, str)

        self.assertEqual(config['name'], tt.name)
        self.assertEqual(h.root_node.value, tt.hierarchy.root_node.value)
        self.assertEqual(h.leaf_nodes[0].value, tt.hierarchy.leaf_nodes[0].value)
