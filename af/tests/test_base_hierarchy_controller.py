import json
import unittest

from af.model.hierarchies.BaseHierarchy import BaseHierarchy
from af.model.hierarchies.Node import Node
from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController

class TestBaseHierarchyController(unittest.TestCase):

    def setUp(self):
        self.h = BaseHierarchy()
        self.bh_controller = BaseHierarchyController(self.h)

    def test_correct_hierarchy_association(self):

        self.assertEqual(self.h, self.bh_controller.hierarchy, "Hierarchies do not match")

    def test_load_generalization_hierarchy_ok(self):
        json_saved_hierarchy = {"**********": {1: {2: 3}}}

        hierarchy_loaded = self.bh_controller.load_hierarchy(json_saved_hierarchy, attribute_type=int)

        self.assertTrue(len(hierarchy_loaded.leaf_nodes) == 1, "There should be only 1 leaf node")
        self.assertEqual(3, hierarchy_loaded.leaf_nodes[0].value, "The leaf node should have value 3")
        self.assertEqual(2, hierarchy_loaded.leaf_nodes[0].parent.value, "The parent of the leaf node should have value 2")
        self.assertTrue('*' in hierarchy_loaded.root_node.value, "The root node should be the supression default")
        self.assertTrue(len(hierarchy_loaded.root_node.nodes) == 1, "The root node should have only one node son")
        self.assertEqual(1, hierarchy_loaded.root_node.nodes[0].value, "The son of the root node should have value 1")

    def test_load_supression_hierarchy_ok(self):
        json_saved_hierarchy = "**********"

        hierarchy_loaded = self.bh_controller.load_hierarchy(json_saved_hierarchy, attribute_type=int)

        self.assertTrue(len(hierarchy_loaded.leaf_nodes) == 1, "There should be only 1 leaf node")

    def test_get_json_representation_no_hierarchy(self):
        expected = None
        bh_controller = BaseHierarchyController(None)

        self.assertEqual(expected, bh_controller.get_hierarchy_representation())

    def test_get_json_representation_supression_hierarchy(self):
        expected = "**********"

        self.assertEqual(expected, self.bh_controller.get_hierarchy_representation())

    def test_get_json_representation_generalization_hierarchy(self):
        n = Node(1)
        self.h.add_node(self.h.root_node, n)

        expected = {"**********": 1}

        self.assertEqual(expected, self.bh_controller.get_hierarchy_representation())
