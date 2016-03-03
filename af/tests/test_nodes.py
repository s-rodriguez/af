import unittest
from af.model.hierarchies.BaseHierarchy import Node


class TestNodes(unittest.TestCase):

    def test_node_creation_ok(self):
        value = 123
        parent = None
        leaf_nodes = [1,2,3]

        node = Node(value, parent, leaf_nodes)

        self.assertEqual(value, node.value, "Different node value")
        self.assertEqual(parent, node.parent, "Different node parent")
        self.assertEqual(leaf_nodes, node.nodes, "Different node leaf nodes")
