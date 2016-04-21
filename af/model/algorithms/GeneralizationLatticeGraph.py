import itertools


class GLGNode:
    """This class is intended for the modelization of Node inside a GeneralizationLatticeGraph.
    A GLGNode contains information about the level in which it is placed, the subset dimension values of it, and if it is marked as a valid node to be used for anonymization or not.

    """
    def __init__(self, subset, glg_lvl, qi_keys, marked=False):
        self.subset = subset
        self.glg_lvl = glg_lvl
        self.qi_keys = qi_keys
        self.marked = marked

    def __repr__(self):
        subset = {}
        for key, dimension in zip(self.qi_keys, self.subset):
            subset[key] = dimension
        return str({'subset': subset, 'marked': self.marked})


class GeneralizationLatticeGraph:
    """This class is used to create a graph that relates all the dimension combination nodes within each other.
    In particular, it is used to know, given a certain GLGNode (That is basically a subset of combinations of all the qi attributes values), which are the GLGNodes connected to it.

    """
    def __init__(self, qi_info):
        # qi_info example: [('birth', (0, 1)) , ('zip', (0, 1, 2)), ('sex', (0, 1))]
        self.qi_info = qi_info
        self.qi_keys = None
        self.bfs_level_nodes = None
        self.create_bfs_structure()

    def create_bfs_structure(self):
        """Creates the BFS structure to be used later during the anonymization process.
        It maintains a cache list of all the leaf nodes that appeared.

        """
        self.qi_keys = []
        list_of_lvls = []

        for qi_tuple in self.qi_info:
            qi_key, qi_lvls = qi_tuple
            self.qi_keys.append(qi_key)
            list_of_lvls.append(qi_lvls)

        self.bfs_level_nodes = {}

        for subset in itertools.product(*list_of_lvls):
            lvl = sum(subset)
            if lvl not in self.bfs_level_nodes.keys():
                self.bfs_level_nodes[lvl] = []
            self.bfs_level_nodes[lvl].append(GLGNode(subset=subset, glg_lvl=lvl, qi_keys=self.qi_keys, marked=False))

    def get_lvl_subnodes(self, lvl):
        """Return all the GLGNodes that are in that specific level.

        :param int lvl: Level inteded to analyze
        :rtype: List of GLGNodes

        """
        # Reached the highest possible level
        if lvl not in self.bfs_level_nodes.keys():
            return None
        return self.bfs_level_nodes[lvl]

    def get_upper_level_nodes(self, node, lvl):
        """Return all the nodes that are above a certain GLGNode and a certain lvl.

        :param node: GLGNode intended to be used to find it's upper nodes
        :param int lvl: Level in which the node is located
        :rtype: List of GLGNodes that are parents of the node

        """
        upper_level_nodes = []
        possible_upper_nodes = self.get_lvl_subnodes(lvl)
        if possible_upper_nodes:
            for upper_node in possible_upper_nodes:
                condition1 = sum(upper_node.subset)-sum(node.subset) == 1
                condition2 = all(0 <= t[1]-t[0] <= 1 for t in zip(node.subset, upper_node.subset))
                if all((condition1, condition2)):
                    upper_level_nodes.append(upper_node)
        return upper_level_nodes

    def mark_valid_subnode(self, node):
        """Given a node, mark it as a valid option to be used during the anonymization process

        :param node: GLGNode to be marked as valid

        """
        node.marked = True
        current_lvl = sum(node.subset)
        for upper_node in self.get_upper_level_nodes(node, current_lvl+1):
            self.mark_valid_subnode(upper_node)

    def get_marked_nodes(self, marked=True):
        """Return a list of all those GLGNodes inside the GeneralizationLatticeGraph that are marked with a certain value.

        :param bool marked: True or False (Default to True)
        :rtype: List of nodes that are marked as required.

        """
        marked_nodes = []
        lvl = 0
        finished = False

        while not finished:
            nodes = self.get_lvl_subnodes(lvl)
            if nodes is None:
                finished = True
            else:
                marked_nodes.extend([node for node in nodes if node.marked == marked])
                lvl += 1
        return marked_nodes
