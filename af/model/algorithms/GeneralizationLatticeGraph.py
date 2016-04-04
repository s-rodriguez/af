import itertools


class GLGNode:
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

    def __init__(self, qi_info):
        # qi_info example: [('birth', (0, 1)) , ('zip', (0, 1, 2)), ('sex', (0, 1))]
        self.qi_info = qi_info
        self.qi_keys = None
        self.bfs_level_nodes = None
        self.create_bfs_structure()

    def create_bfs_structure(self):
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
        # Reached the highest possible level
        if lvl not in self.bfs_level_nodes.keys():
            return None
        return self.bfs_level_nodes[lvl]

    def get_upper_level_nodes(self, node, lvl):
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
        node.marked = True
        current_lvl = sum(node.subset)
        for upper_node in self.get_upper_level_nodes(node, current_lvl+1):
            self.mark_valid_subnode(upper_node)

    def get_marked_nodes(self, marked=True):
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

    @staticmethod
    def test():
        birth_info = ('birth', (0, 1))
        zip_info = ('zip', (0, 1, 2))
        sex_info = ('sex', (0, 1))

        qi_info = (birth_info, zip_info, sex_info)
        glg = GeneralizationLatticeGraph(qi_info)
        print "Get qi keys"
        print glg.qi_keys

        print "\nGet glg representation"
        for lvl, subsets in glg.bfs_level_nodes.iteritems():
            print "Level: "+str(lvl)+": "+str(subsets)

        print "\nGet lvl subsets at request"
        for lvl in range(0, 6):
            print "Level: "+str(lvl)
            print "Subsets :  "+str(glg.get_lvl_subnodes(lvl))

        print "\nMark all nodes as read"
        glg.mark_valid_subnode(glg.bfs_level_nodes[1][1])
        for lvl in range(0, 6):
            print "Level: "+str(lvl)
            print "Subsets :  "+str(glg.get_lvl_subnodes(lvl))

if __name__ == "__main__":
    # GLG Test
    GeneralizationLatticeGraph.test()
