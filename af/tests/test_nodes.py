import unittest
from af.model.hierarchies.Node import Node


class TestNodes(unittest.TestCase):

    def test_node_creation_ok(self):
        value = 123
        parent = None
        leaf_nodes = [1,2,3]

        node = Node(value, parent, leaf_nodes)

        self.assertEqual(value, node.value, "Different node value")
        self.assertEqual(parent, node.parent, "Different node parent")
        self.assertEqual(leaf_nodes, node.nodes, "Different node leaf nodes")
        self.assertTrue(node.is_root(), "Should be a root node")
        self.assertFalse(node.is_leaf(), "Should not be a leaf")

    def test_remove_node_ok(self):
        value = 123
        parent = None
        son_node = 1
        leaf_nodes = [son_node]

        node = Node(value, parent, leaf_nodes)

        self.assertTrue(len(node.nodes) == 1, "Node should have 1 son node")
        node.remove_node(son_node)
        self.assertTrue(node.nodes == None, "Node should no son nodes")

    def test_representation(self):
        val = 1
        n = Node(val)

        self.assertEqual(str(val), n.__repr__(), "Representation should be the node value")
