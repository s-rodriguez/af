import unittest
from af.model.hierarchies.BaseHierarchy import BaseHierarchy
from af.model.hierarchies.Node import Node

class TestHierarchies(unittest.TestCase):

    def test_hierarchy_should_have_supression_node_by_default(self):

        hierarchy = BaseHierarchy()

        self.assertTrue(hierarchy.root_node is not None, "Hierarchy base node should not be None")
        self.assertTrue(isinstance(hierarchy.root_node, Node), "Root node should be a Node")
        self.assertTrue('*' in hierarchy.root_node.value, "Root node should have * as value")
        self.assertTrue(len(hierarchy.leaf_nodes) == 1, "Root node should be added to the leaf nodes")

    def test_adding_nodes_ok(self):

        hierarchy = BaseHierarchy()
        node = Node(1)

        hierarchy.add_node(hierarchy.root_node, node)

        self.assertTrue(len(hierarchy.leaf_nodes) == 1, "Hierarchy should have only one leaf node after addition")
        self.assertEqual(node, hierarchy.leaf_nodes[0], "The leaf node should be the one added")
        self.assertTrue(node in hierarchy.root_node.nodes, "New node should be son of root node")
        self.assertTrue(node.parent == hierarchy.root_node, "New node should have root node as parent")

    def test_finding_nodes_ok(self):
        hierarchy = BaseHierarchy()
        node = Node(1)
        hierarchy.add_node(hierarchy.root_node, node)

        finded_node = hierarchy.find_node(node.value)
        self.assertEqual(node, finded_node, "Not the same node found")


    def test_get_generalization_level_ok(self):
        hierarchy = BaseHierarchy()
        node1 = Node(1)
        node2 = Node(2)
        hierarchy.add_node(hierarchy.root_node, node1)
        hierarchy.add_node(node1, node2)

        gen_node_0 = hierarchy.get_generalization_level_representation(node2, 0)
        gen_node_1 = hierarchy.get_generalization_level_representation(node2, 1)
        gen_node_2 = hierarchy.get_generalization_level_representation(node2, 2)

        self.assertEqual(gen_node_0, node2, "Should be the same node")
        self.assertEqual(gen_node_1, node1, "Should be the same node")
        self.assertEqual(gen_node_2, hierarchy.root_node, "Should be the same node")
