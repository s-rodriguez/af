import unittest
from af.model.hierarchies.BaseHierarchy import BaseHierarchy
from af.model.hierarchies.Node import Node
from af.exceptions import InfoException


class TestHierarchies(unittest.TestCase):

    def setUp(self):
        self.h = BaseHierarchy()
        self.saved_hierarchy = {1: {2: {3: None}}}

    def test_hierarchy_should_have_supression_node_by_default(self):
        self.assertTrue(self.h.root_node is not None, "Hierarchy base node should not be None")
        self.assertTrue(isinstance(self.h.root_node, Node), "Root node should be a Node")
        self.assertEqual(BaseHierarchy.supression_node().value, self.h.root_node.value, "Root node should have * as value")
        self.assertTrue(len(self.h.leaf_nodes) == 1, "Root node should be added to the leaf nodes")

    def test_supression_node_ok(self):
        sup_node = self.h.create_supression_node()

        self.assertEqual(BaseHierarchy.supression_node().value, sup_node.value, "Root node should be * x 10")
        self.assertEqual(None, sup_node.parent, "Root node should have no parent on creation")
        self.assertEqual(None, sup_node.nodes, "Root node should have no leaf nodes on creation")

    def test_get_leaf_node_ok(self):
        leaf_node = self.h.get_leaf_node(self.h.root_node.value)

        self.assertEqual(self.h.root_node, leaf_node, "The leaf node found should be the root")

    def test_adding_nodes_ok(self):
        node = Node(1)

        self.h.add_node(self.h.root_node, node)

        self.assertTrue(len(self.h.leaf_nodes) == 1, "Hierarchy should have only one leaf node after addition")
        self.assertEqual(node, self.h.leaf_nodes[0], "The leaf node should be the one added")
        self.assertTrue(node in self.h.root_node.nodes, "New node should be son of root node")
        self.assertTrue(node.parent == self.h.root_node, "New node should have root node as parent")

    def test_finding_nodes_ok(self):
        node = Node(1)

        self.h.add_node(self.h.root_node, node)

        found_node = self.h.find_node(node.value)
        self.assertEqual(node, found_node, "Not the same node found")

    def test_maintain_leaf_nodes_ok(self):
        node = Node(22)

        self.h.maintain_leaf_nodes(node, 'add')

        self.assertTrue(len(self.h.leaf_nodes) == 2, "Hierarchy should have only one leaf node after addition")
        self.assertEqual(node, self.h.leaf_nodes[1], "The node should be among the leaf nodes")

        self.h.maintain_leaf_nodes(node, 'remove')

        self.assertTrue(len(self.h.leaf_nodes) == 1, "Hierarchy should have only one leaf node after addition")
        self.assertEqual(self.h.root_node, self.h.leaf_nodes[0], "Leaf nodes should contain only the root node")

    def test_maintain_leaf_nodes_raise_exception_unknown_action(self):
        failed = False
        try:
            node = Node(22)
            self.h.maintain_leaf_nodes(node, 'asdfasdfsadf')
        except Exception:
            failed = True

        self.assertTrue(failed, "Method should have failed")

    def test_get_generalization_level_ok(self):
        node1 = Node(1)
        node2 = Node(2)

        self.h.add_node(self.h.root_node, node1)
        self.h.add_node(node1, node2)

        gen_node_0 = self.h.get_generalization_level_representation(node2, 0)
        gen_node_1 = self.h.get_generalization_level_representation(node2, 1)
        gen_node_2 = self.h.get_generalization_level_representation(node2, 2)
        gen_node_3 = self.h.get_generalization_level_representation(node2, 3)

        self.assertEqual(gen_node_0, node2, "Should be the same node")
        self.assertEqual(gen_node_1, node1, "Should be the same node")
        self.assertEqual(gen_node_2, self.h.root_node, "Should be the same node")
        self.assertEqual(gen_node_3, self.h.root_node, "Should be the same node")

    def test_hierarchy_representation_ok(self):
        node1 = Node(1)
        self.h.add_node(self.h.root_node, node1)

        representation_expected = {self.h.root_node.value: {node1.value: None}}

        self.assertEqual(representation_expected, self.h.hierarchy_representation(), "The representations don't match")

    def test_populate_nodes_ok(self):
        self.h.populate_nodes(self.h.root_node, self.saved_hierarchy, int)

        self.assertTrue(len(self.h.leaf_nodes) == 1, "There should be only one leaf node")
        self.assertEqual(3, self.h.leaf_nodes[0].value, "The leaf node should be of value 3")

        self.assertTrue(len(self.h.root_node.nodes) == 1, "The root node should have only one node")
        self.assertEqual(1, self.h.root_node.nodes[0].value, "The values dont match")

    def test_transform_supression_ok(self):
        t0 = self.h.transform(3, 0)
        t1 = self.h.transform(3, 1)

        self.assertEqual(3, t0, 'Supression level 0 should be the same value')
        self.assertEqual(self.h.root_node.value, t1, 'Supression level above 0 should be suression node')

    def test_transform_generalization_ok(self):
        self.h.populate_nodes(self.h.root_node, self.saved_hierarchy, int)

        t0 = self.h.transform(3, 0)
        t1 = self.h.transform(3, 1)
        t2 = self.h.transform(3, 2)
        t3 = self.h.transform(3, 3)

        self.assertEqual(3, t0, 'Generalization value dont match')
        self.assertEqual(2, t1, 'Generalization value dont match')
        self.assertEqual(1, t2, 'Generalization value dont match')
        self.assertEqual(self.h.root_node.value, t3, 'Generalization value dont match')

    def test_cannot_transform_inexistent_value_on_generalization_hierarchy(self):
        node1 = Node(1)

        self.h.add_node(self.h.root_node, node1)

        raised_exception = False
        try:
            self.h.transform(33, 1)
        except InfoException:
            raised_exception = True

        self.assertTrue(raised_exception, 'An exception should have been raised')

    def test_hierarchy_depth_ok_leaf_nodes(self):
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)

        self.h.add_node(self.h.root_node, node1)
        self.h.add_node(node1, node2)
        self.h.add_node(node1, node3)

        node4 = Node(4)
        node5 = Node(5)
        self.h.add_node(node2, node4)
        self.h.add_node(node3, node5)
        self.assertTrue(self.h.validate_hierarchy_depth())

    def test_hierarchy_depth_ok_only_root(self):
        node1 = Node(1)
        self.h.add_node(self.h.root_node, node1)
        self.assertTrue(self.h.validate_hierarchy_depth())

    def test_hierarchy_depth_failed(self):
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)

        self.h.add_node(self.h.root_node, node1)
        self.h.add_node(node1, node2)
        self.h.add_node(node1, node3)

        node4 = Node(4)
        node5 = Node(5)
        self.h.add_node(node2, node4)
        self.h.add_node(node2, node5)

        self.assertFalse(self.h.validate_hierarchy_depth())
