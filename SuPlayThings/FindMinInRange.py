
INT_MAX = 99


class TreeNode:
    def __init__(self, l, r, val=None, l_child=None, r_child=None):
        self.l = l
        self.r = r
        self.val = val
        self.l_child = l_child
        self.r_child = r_child
        print("tree node created: {}-{}, val: {}, l_child: {}, r_child: {}".format(
            str(self.l), str(self.r), str(self.val), str(self.l_child), str(self.r_child)))


def find_min_in_range(arr, start, end):

    def create_tree(start, end):
        print("create_tree: start = {}, end = {}".format(str(start), str(end)))
        if start == end:
            return TreeNode(start, end, arr[start])
        mid = (start + end) >> 1
        l_child = create_tree(start, mid)
        r_child = create_tree(mid+1, end) if mid+1 <= end else None
        l_min = l_child.val
        r_min = r_child.val if r_child else INT_MAX
        return TreeNode(start, end, min(l_min, r_min), l_child, r_child)

    def query_min(node, start, end):
        if not node:
            print("empty node, return INT_MAX")
            return INT_MAX
        print("querying: node = ({}, {}) -> {}, start, end = ({}, {})".format(
            str(node.l), str(node.r), str(node.val), str(start), str(end)))
        if start > node.r or end < node.l or end < start:
            print("returning INT_MAX")
            return INT_MAX
        if start <= node.l <= node.r <= end:
            print("****** MEANINGFUL ****** returning node.val = {}".format(str(node.val)))
            return node.val
        return min(query_min(node.l_child, start, end), query_min(node.r_child, start, end))

    def print_tree(node, depth=0):
        if not node:
            return
        print("----" * depth + " ({}, {}) -> {}".format(str(node.l), str(node.r), str(node.val)))
        print_tree(node.l_child, depth+1)
        print_tree(node.r_child, depth+1)

    root = create_tree(0, len(arr)-1)
    print_tree(root)
    return query_min(root, start, end)
#
#                                         [0, 8, None]
#                     [0, 4, 1]                            [5, 8, 1]
#             [0, 2, 1]        [3, 4, 1]                      ...........
#     [0, 1, 1]    [2, 2, 3] [3, 3, 1] [4, 4, 5]
# [0, 0, 2]   [1, 1, 1]

test_1 = [2, 1, 3, 1, 5, 6, 3, 4, 1]
start = 4
end = 6
expected = 3

assert(expected == find_min_in_range(test_1, start, end))