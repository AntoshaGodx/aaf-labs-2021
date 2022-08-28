from node import Node


class RDTree:
    root = None

    @staticmethod
    def compare(set1, set2):
        return len(set1.intersection(set2))

    @staticmethod
    def create_node(data):
        return Node(data)

    def insert(self, node, data):
        if not node:
            return self.create_node(data)
        self.root = node
        if node.left or node.right:
            if self.compare(node.left.value, data) > self.compare(node.right.value, data):
                node.value = node.value.union(data)
                self.insert(node.left, data)
            else:
                node.value = node.value.union(data)
                self.insert(node.right, data)
        else:
            node.left = self.create_node(node.value)
            node.value = node.value.union(data)
            node.right = self.create_node(data)
        return node

    @staticmethod
    def get_leaf_nodes(start_node):
        leaves = []

        def _get_leaf_nodes(node):
            if node is not None:
                if not (node.left or node.right):
                    leaves.append(node.value)
                _get_leaf_nodes(node.left)
                _get_leaf_nodes(node.right)

        _get_leaf_nodes(start_node)
        return leaves

    def contains(self, node: Node, data: set) -> bool:
        res = False
        if node:
            if node.value == data and not (node.left or node.right):
                return True
            if data.issubset(node.value):
                res = self.contains(node.right, data)
                if res:
                    return res
                res = self.contains(node.left, data)
                if res:
                    return res
        return res

    def search_contains(self, node: Node, data: set):
        res = []

        def _search_contains(node, data):
            if data.issubset(node.value):
                if not (node.left or node.right):
                    return node.value
                tmp = _search_contains(node.right, data)
                if tmp:
                    res.append(tmp)
                tmp = _search_contains(node.left, data)
                if tmp:
                    res.append(tmp)

        _search_contains(node, data)
        return res

    def search_intersects(self, node, data):
        res = []

        def _search_intersects(node, data):
            if data.intersection(node.value) != set():
                if not (node.left or node.right):
                    return node.value
                tmp = _search_intersects(node.right, data)
                if tmp:
                    res.append(tmp)
                tmp = _search_intersects(node.left, data)
                if tmp:
                    res.append(tmp)

        _search_intersects(node, data)
        return res

    def search_contained_by(self, node, data):
        res = []
        intersects = self.search_intersects(node, data)
        for st in intersects:
            if st.issubset(data):
                res.append(st)
        return res

    def print_tree(self, node, level=0):
        if node:
            if level != 0:
                print('|   ' * level + 'L_', node.value)
            else:
                print(' ' * 4 * level + 'L_', node.value)
            self.print_tree(node.left, level + 1)
            self.print_tree(node.right, level + 1)

    def convert_tree_to_dict(self, node):
        tree = {}

        def _convert_tree_to_dict(node):
            if not (node.left or node.right):
                return tree
            tree[str(node.value)] = {str(node.left.value), str(node.right.value)}
            _convert_tree_to_dict(node.left)
            _convert_tree_to_dict(node.right)

        _convert_tree_to_dict(node)
        return tree

    def print_dependency_tree(self, tree, root, *, indent=0, ctx=None):     #stackoverflow
        # """
        # >>> tree = {"a": {"b", "c"},
        # >>>         "b": {"d"},
        # >>>         "c": {"b", "d"}}
        # >>> print_dependency_tree(tree, "a")
        # a
        # ├─b
        # │ └─d
        # └─c
        #   ├─b
        #   │ └─d
        #   └─d
        # """
        depth, branches, seen = ctx or (0, [], set())
        if depth == 0:
            print(" " * indent + root)
        if root not in tree:
            return
        branches += [None]
        seen |= {root}
        children = set(tree[root]) - seen
        more = len(children)
        for child in sorted(children):
            more -= 1
            branches[depth] = ("├" if more else "└") + "─"
            if child in seen:
                continue
            print(" " * indent + "".join(branches) + child)
            if child in tree:
                branches[depth] = ("│" if more else " ") + " "
                ctx = depth + 1, branches.copy(), seen.copy()
                self.print_dependency_tree(tree, child, indent=indent, ctx=ctx)


def main():
    pass


if __name__ == "__main__":
    main()
