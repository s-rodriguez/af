import random

from af.model.hierarchies.BaseHierarchy import Node, BaseHierarchy
from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController

def create_hierarchy():
    root_node = Node(0)
    baseh = BaseHierarchy(root_node, [])

    for i in range(0, 3):
        n = Node(random.randint(1,100))
        baseh.add_node(root_node, n)
        for i in range(0, 2):
            n2 = Node(random.randint(1,100))
            baseh.add_node(n, n2)
            for i in range(0, 1):
                n3 = Node(random.randint(1,100))
                baseh.add_node(n2, n3)

    return BaseHierarchyController(baseh)

def load(config):
    return BaseHierarchyController.load_hierarchy(config)

