import argparse
import random

from af.model.hierarchies.BaseHierarchy import Node, BaseHierarchy
from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController

def create_hierarchy():
    baseh = BaseHierarchy()
    root_node = Node(0)

    baseh.add_node(baseh.root_node, root_node)

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
    bhc = BaseHierarchyController()
    bhc.load_hierarchy(config, int)
    return bhc


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-play', type=int, action='store', dest='play')

    results = parser.parse_args()

    play = 2

    if results.play == 1 or play == 1:
        h = create_hierarchy()
        with open('test', 'w+') as f:
            f.write(h.get_json_representation())
    else:
        with open('test', 'r+') as f:
            config = f.read()
        bhc = load(config)
        print bhc.get_json_representation()

