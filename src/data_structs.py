from typing import List, Set, Optional, Tuple

import numpy as np


class TreeNode:
    def __init__(self, index: int, bin_index_vals: Set[int], verbose_name: str):
        self.count = 0
        self.index = index
        self.verbose_name = verbose_name
        self.bin_index_vals = bin_index_vals
        self.select_array = None
        self.update_bit_string()

    def update_bit_string(self):
        bit_array = np.zeros(256, dtype=int)
        for bin_index in self.bin_index_vals:
            bit_array[bin_index] = 1
        self.select_array = np.packbits(bit_array).view(np.uint32)

    def add_binary_indicies(self, indicies: Set[int]):
        self.bin_index_vals.update(indicies)
        self.update_bit_string()


class Tree:
    def __init__(self, branch_factor: int, verbose_name: str, levels: int = 2):
        self.branching_factor = branch_factor
        self.node_list: List[Optional[TreeNode]] = [None] * ((branch_factor ** (levels-1)) + 1)
        self.node_list[0] = TreeNode(index=0, bin_index_vals=set(), verbose_name="ALL" + verbose_name)

    def remove_node(self, to_remove: TreeNode):
        pass

    def add_node(self, index: int, bin_index_vals: Set[int], verbose_name: str):
        new_node = TreeNode(index, bin_index_vals, verbose_name)
        self.node_list[index] = new_node
        # update parent binary lists
        curr = self.get_parent_node(new_node)
        while curr:
            curr.add_binary_indicies(new_node.bin_index_vals)
            curr = self.get_parent_node(curr)

    def get_parent_node(self, curr: TreeNode) -> Optional[TreeNode]:
        parent_index = (curr.index - 1) // self.branching_factor
        if parent_index >= 0:
            return self.node_list[parent_index]
        return None

    def get_children(self, curr: TreeNode) -> List[TreeNode]:
        first_child_index = (curr.index * self.branching_factor) + 1
        last_child_index = (curr.index * self.branching_factor) + (self.branching_factor - 1)
        if last_child_index >= len(self.node_list):
            return []
        else:
            return [x for x in self.node_list[first_child_index: last_child_index + 1] if x]


def create_basic_tree(values: List[Tuple[int, str]], verbose_name: str) -> Tree:
    """
    Creates a very basic 2 level tree with 1 ALL_x node at the top,
    and all other nodes (indicated by the list of tuples provided) in the second level
    """
    the_tree = Tree(len(values), verbose_name)
    for i, (binary_index, name) in enumerate(values):
        the_tree.add_node(i+1, {binary_index}, verbose_name + "_" + name)
    return the_tree
